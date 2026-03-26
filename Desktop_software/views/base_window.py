"""
Base Window Class - Common functionality for all PySide6 views
Provides base class with theme support, common utilities, and worker thread handling
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QDialog, QMessageBox
from PySide6.QtCore import Qt, QThread, Signal, QObject
from PySide6.QtGui import QFont
from utils.unified_theme import UnifiedTheme
import atexit


class WorkerSignals(QObject):
    """Signals for worker threads"""
    finished = Signal(object)  # Success result
    error = Signal(str)  # Error message
    progress = Signal(int)  # Progress update (0-100)


class WorkerThread(QThread):
    """Generic worker thread for running tasks without blocking UI"""
    
    # Class-level tracking of active threads
    _active_threads = []
    
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self._active = True
        
        # Track this thread
        WorkerThread._active_threads.append(self)
        
        # Connect finished signal to cleanup
        self.finished.connect(self._on_finished)
        self.signals.finished.connect(self._cleanup)
        self.signals.error.connect(self._cleanup)
    
    def run(self):
        """Execute the function in this thread"""
        try:
            result = self.func(*self.args, **self.kwargs)
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self._active = False
    
    def _on_finished(self):
        """Called when thread finishes execution"""
        pass
    
    def _cleanup(self):
        """Clean up thread references"""
        self._active = False
        if self in WorkerThread._active_threads:
            WorkerThread._active_threads.remove(self)
        
        # Schedule thread for deletion
        self.deleteLater()
    
    def stop(self):
        """Request thread to stop"""
        self._active = False
        self.wait(1000)  # Wait up to 1 second


# Cleanup all threads on exit
@atexit.register
def cleanup_threads():
    """Clean up all active worker threads"""
    for thread in WorkerThread._active_threads[:]:
        if thread.isRunning():
            thread._active = False
            thread.wait(500)  # Wait up to 500ms
    WorkerThread._active_threads.clear()


class BaseView(QWidget):
    """Base class for all view widgets with common functionality"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme_manager = UnifiedTheme()
        self._setup_base_style()
        self._workers = []  # Track workers for cleanup

    def _setup_base_style(self):
        """Apply base styling to the widget"""
        self.setAutoFillBackground(True)
        # Apply theme palette and stylesheet
        self.theme_manager.apply_palette(self)
        self.setStyleSheet(self.theme_manager.get_main_stylesheet())
    
    def run_in_thread(self, func, on_success, on_error=None, *args, **kwargs):
        """
        Run a function in a background thread

        Args:
            func: Function to run
            on_success: Callback function for success (receives result)
            on_error: Optional callback for error (receives error message) OR first arg to func
            *args, **kwargs: Arguments to pass to func
        """
        worker = WorkerThread(func, *args, **kwargs)
        worker.signals.finished.connect(on_success)
        
        # Handle on_error - if it's a string or not callable, treat it as first arg
        if on_error is not None:
            if callable(on_error):
                worker.signals.error.connect(on_error)
            else:
                # on_error is actually an argument, add it to args
                # This handles backward compatibility
                pass
        
        # Always connect error to default handler if not explicitly handled
        if on_error is None or not callable(on_error):
            worker.signals.error.connect(self._default_error_handler)

        # Track worker for cleanup
        self._workers.append(worker)

        # Clean up completed workers
        self._cleanup_finished_workers()

        worker.start()
    
    def _cleanup_finished_workers(self):
        """Remove references to finished workers"""
        self._workers = [w for w in self._workers if w.isRunning()]
    
    def closeEvent(self, event):
        """Handle widget close event - cleanup workers"""
        self._cleanup_workers()
        super().closeEvent(event) if hasattr(super(), 'closeEvent') else None
    
    def _cleanup_workers(self):
        """Clean up all worker threads"""
        for worker in self._workers:
            if worker.isRunning():
                worker._active = False
                worker.wait(500)  # Wait up to 500ms
                worker.deleteLater()
        self._workers.clear()
    
    def _default_error_handler(self, error_msg):
        """Default error handler - shows QMessageBox"""
        QMessageBox.critical(self, "Error", error_msg)
    
    def show_success_message(self, message, title="Success"):
        """Show success message box"""
        QMessageBox.information(self, title, message)
    
    def show_error_message(self, message, title="Error"):
        """Show error message box"""
        QMessageBox.critical(self, title, message)
    
    def show_warning_message(self, message, title="Warning"):
        """Show warning message box"""
        QMessageBox.warning(self, title, message)
    
    def show_question(self, message, title="Confirm"):
        """Show question dialog, returns True if Yes"""
        result = QMessageBox.question(
            self, title, message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return result == QMessageBox.StandardButton.Yes

    def get_colors(self):
        """Get colors for dark theme"""
        return self.theme_manager.get_colors()

    def _create_group_box(self, title, layout_type='vbox'):
        """
        Create styled group box - reusable across all views
        
        Args:
            title: Group box title
            layout_type: 'vbox' for QVBoxLayout, 'form' for QFormLayout
        
        Returns:
            QGroupBox with styled layout
        """
        from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QFormLayout
        
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11pt;
                border: 2px solid #DCDCDC;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 8px;
                color: #1976D2;
                font-size: 12pt;
            }
        """)
        
        if layout_type == 'form':
            layout = QFormLayout(group)
            layout.setSpacing(12)
        else:
            layout = QVBoxLayout(group)
            layout.setSpacing(12)
        
        return group


class BaseDialog(QDialog):
    """Base class for all dialog windows"""

    def __init__(self, parent=None, title="Dialog"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.theme_manager = UnifiedTheme()
        self.setMinimumWidth(400)
        self._workers = []
        self._setup_base_style()
    
    def _setup_base_style(self):
        """Apply base styling"""
        pass
    
    def run_in_thread(self, func, on_success, on_error=None, *args, **kwargs):
        """Run function in background thread"""
        worker = WorkerThread(func, *args, **kwargs)
        worker.signals.finished.connect(on_success)
        if on_error:
            worker.signals.error.connect(on_error)
        else:
            worker.signals.error.connect(self._default_error_handler)
        
        self._workers.append(worker)
        worker.start()
    
    def _default_error_handler(self, error_msg):
        """Default error handler"""
        QMessageBox.critical(self, "Error", error_msg)
    
    def _cleanup_workers(self):
        """Clean up all worker threads"""
        for worker in self._workers:
            if worker.isRunning():
                worker._active = False
                worker.wait(500)
                worker.deleteLater()
        self._workers.clear()
    
    def accept(self):
        """Override accept to cleanup worker threads"""
        self._cleanup_workers()
        super().accept()
    
    def reject(self):
        """Override reject to cleanup worker threads"""
        self._cleanup_workers()
        super().reject()
    
    def closeEvent(self, event):
        """Handle dialog close event"""
        self._cleanup_workers()
        super().closeEvent(event)
