"""
Image Upload Optimization Module
Handles image compression, resizing, and safe upload processing
Uses Pillow for image manipulation
"""

from PIL import Image
import io
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ImageOptimizer:
    """Optimize images for web upload"""
    
    # Maximum dimensions for different image types
    MAX_DIMENSIONS = {
        'gallery': (1920, 1080),  # Full HD max
        'product': (1200, 1200),   # Square product images
        'thumbnail': (400, 400),   # Thumbnail size
        'avatar': (200, 200)       # Profile pictures
    }
    
    # Quality settings (1-100, higher = better quality)
    QUALITY_SETTINGS = {
        'gallery': 85,
        'product': 90,
        'thumbnail': 80,
        'avatar': 85,
        'default': 85
    }
    
    # Maximum file size (5MB)
    MAX_FILE_SIZE = 5 * 1024 * 1024
    
    def __init__(self, upload_folder):
        """
        Initialize image optimizer
        
        Args:
            upload_folder: Base folder for uploads
        """
        self.upload_folder = upload_folder
        self.gallery_folder = os.path.join(upload_folder, 'gallery')
        
        # Create folders if they don't exist
        os.makedirs(self.upload_folder, exist_ok=True)
        os.makedirs(self.gallery_folder, exist_ok=True)
    
    def optimize_image(self, image_file, image_type='gallery', max_size_kb=None):
        """
        Optimize an image for web upload
        
        Args:
            image_file: File object from upload
            image_type: Type of image (gallery, product, thumbnail, avatar)
            max_size_kb: Maximum file size in KB (optional)
        
        Returns:
            dict: {
                'success': bool,
                'image_data': bytes (optimized image),
                'original_size': int (bytes),
                'optimized_size': int (bytes),
                'compression_ratio': float (percentage),
                'dimensions': tuple (width, height),
                'format': str (image format),
                'error': str (if failed)
            }
        """
        try:
            # Get original file size
            image_file.seek(0, 2)  # Seek to end
            original_size = image_file.tell()
            image_file.seek(0)  # Reset to beginning
            
            # Check file size
            if original_size > self.MAX_FILE_SIZE:
                return {
                    'success': False,
                    'error': f'File too large. Maximum size is {self.MAX_FILE_SIZE // 1024 // 1024}MB'
                }
            
            # Open image with Pillow
            img = Image.open(image_file)
            
            # Convert to RGB if necessary (handles PNG with transparency, etc.)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparent images
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get maximum dimensions for this image type
            max_width, max_height = self.MAX_DIMENSIONS.get(
                image_type, self.MAX_DIMENSIONS['default']
            )
            
            # Resize if necessary
            original_width, original_height = img.size
            if original_width > max_width or original_height > max_height:
                # Calculate new dimensions maintaining aspect ratio
                ratio = min(max_width / original_width, max_height / original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                logger.info(f"Resized image from {original_width}x{original_height} to {new_width}x{new_height}")
            
            # Get quality setting
            quality = self.QUALITY_SETTINGS.get(image_type, self.QUALITY_SETTINGS['default'])
            
            # Compress and save to bytes
            output = io.BytesIO()
            img.save(
                output,
                format='JPEG',
                quality=quality,
                optimize=True,
                progressive=True
            )
            
            # Get optimized size
            optimized_size = output.tell()
            output.seek(0)
            
            # Calculate compression ratio
            compression_ratio = ((original_size - optimized_size) / original_size) * 100 if original_size > 0 else 0
            
            logger.info(
                f"Image optimized: {original_size:,} bytes → {optimized_size:,} bytes "
                f"({compression_ratio:.1f}% reduction)"
            )
            
            # Check if we need to reduce quality further to meet size limit
            if max_size_kb and optimized_size > max_size_kb * 1024:
                logger.info(f"Image still too large, reducing quality...")
                return self._reduce_quality(output, img, max_size_kb * 1024)
            
            return {
                'success': True,
                'image_data': output.getvalue(),
                'original_size': original_size,
                'optimized_size': optimized_size,
                'compression_ratio': compression_ratio,
                'dimensions': img.size,
                'format': 'JPEG'
            }
            
        except Exception as e:
            logger.error(f"Image optimization failed: {str(e)}")
            return {
                'success': False,
                'error': f'Image processing failed: {str(e)}'
            }
    
    def _reduce_quality(self, output, img, max_size):
        """
        Reduce image quality to meet size limit
        
        Args:
            output: BytesIO object
            img: PIL Image object
            max_size: Maximum file size in bytes
        
        Returns:
            dict: Optimization result
        """
        for quality in [75, 65, 55, 45]:
            output = io.BytesIO()
            img.save(
                output,
                format='JPEG',
                quality=quality,
                optimize=True,
                progressive=True
            )
            
            if output.tell() <= max_size:
                optimized_size = output.tell()
                output.seek(0)
                
                return {
                    'success': True,
                    'image_data': output.getvalue(),
                    'original_size': img.size[0] * img.size[1] * 3,  # Estimate
                    'optimized_size': optimized_size,
                    'compression_ratio': 0,  # Not accurate in this case
                    'dimensions': img.size,
                    'format': 'JPEG',
                    'quality_reduced': True
                }
        
        # If we can't meet the size limit, return the best we can
        output.seek(0)
        return {
            'success': True,
            'image_data': output.getvalue(),
            'original_size': img.size[0] * img.size[1] * 3,
            'optimized_size': output.tell(),
            'compression_ratio': 0,
            'dimensions': img.size,
            'format': 'JPEG',
            'quality_reduced': True,
            'warning': 'Could not meet size limit, returned best quality'
        }
    
    def save_optimized_image(self, image_data, filename, category='gallery'):
        """
        Save optimized image to disk
        
        Args:
            image_data: Bytes of optimized image
            filename: Filename to save as
            category: Category folder (gallery, products, etc.)
        
        Returns:
            dict: {
                'success': bool,
                'filepath': str (full path),
                'url': str (URL path),
                'size': int (file size in bytes),
                'error': str (if failed)
            }
        """
        try:
            # Determine folder
            folder = os.path.join(self.upload_folder, category)
            os.makedirs(folder, exist_ok=True)
            
            # Create safe filepath
            filepath = os.path.join(folder, filename)
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            # Get file size
            file_size = os.path.getsize(filepath)
            
            # Create URL path
            url_path = f'/uploads/{category}/{filename}'
            
            logger.info(f"Image saved: {filepath} ({file_size:,} bytes)")
            
            return {
                'success': True,
                'filepath': filepath,
                'url': url_path,
                'size': file_size
            }
            
        except Exception as e:
            logger.error(f"Failed to save image: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to save image: {str(e)}'
            }
    
    def process_upload(self, file, category='gallery', custom_filename=None):
        """
        Complete upload processing pipeline
        
        Args:
            file: Uploaded file object
            category: Category for the image
            custom_filename: Optional custom filename
        
        Returns:
            dict: Complete processing result
        """
        from werkzeug.utils import secure_filename
        import secrets
        
        try:
            # Validate file
            if not file or file.filename == '':
                return {'success': False, 'error': 'No file selected'}
            
            # Get file extension
            original_filename = secure_filename(file.filename)
            ext = os.path.splitext(original_filename)[1].lower()
            
            # Validate extension
            allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
            if ext not in allowed_extensions:
                return {
                    'success': False,
                    'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions)}'
                }
            
            # Generate filename
            if custom_filename:
                filename = f"{custom_filename}{ext}"
            else:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                random_str = secrets.token_hex(4)
                filename = f"{timestamp}_{random_str}{ext}"
            
            # Optimize image
            optimization_result = self.optimize_image(file, category)
            
            if not optimization_result['success']:
                return optimization_result
            
            # Save optimized image
            save_result = self.save_optimized_image(
                optimization_result['image_data'],
                filename,
                category
            )
            
            if not save_result['success']:
                return save_result
            
            # Return complete result
            return {
                'success': True,
                'filename': filename,
                'filepath': save_result['filepath'],
                'url': save_result['url'],
                'original_size': optimization_result['original_size'],
                'optimized_size': optimization_result['optimized_size'],
                'compression_ratio': f"{optimization_result['compression_ratio']:.1f}%",
                'dimensions': f"{optimization_result['dimensions'][0]}x{optimization_result['dimensions'][1]}",
                'format': optimization_result['format']
            }
            
        except Exception as e:
            logger.error(f"Upload processing failed: {str(e)}")
            return {
                'success': False,
                'error': f'Upload failed: {str(e)}'
            }


# Create singleton instance (will be initialized in app context)
image_optimizer = None


def get_image_optimizer(upload_folder):
    """Get or create image optimizer instance"""
    global image_optimizer
    if image_optimizer is None:
        image_optimizer = ImageOptimizer(upload_folder)
    return image_optimizer
