"""
Online Request Controller
Handles website form submissions (service requests & contact messages)
"""
from datetime import datetime


class OnlineRequestController:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_all_contact_messages(self, search_term=None, status=None, limit=100):
        """Get all contact messages with optional filters"""
        query = """
        SELECT
            id, name, phone, email, address, service_type, ac_type,
            preferred_date, time_slot, message, status, created_at, updated_at
        FROM contact_messages
        WHERE 1=1
        """
        params = []

        if search_term:
            query += " AND (name LIKE %s OR phone LIKE %s OR email LIKE %s)"
            params.extend([f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"])

        if status:
            query += " AND status = %s"
            params.append(status)

        query += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)

        return self.db.execute_query(query, params, fetch_all=True)

    def update_message_status(self, message_id, status):
        """Update message status"""
        query = """
        UPDATE contact_messages
        SET status = %s, updated_at = NOW()
        WHERE id = %s
        """
        self.db.execute_query(query, (status, message_id))
        return True, f"Status updated to {status}"

    def delete_message(self, message_id):
        """Delete contact message"""
        query = "DELETE FROM contact_messages WHERE id = %s"
        self.db.execute_query(query, (message_id,))
        return True, "Message deleted"

    def get_statistics(self):
        """Get online request statistics"""
        query = """
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN status IN ('unread', 'Pending') THEN 1 ELSE 0 END) as pending,
            SUM(CASE WHEN status IN ('read', 'Contacted') THEN 1 ELSE 0 END) as contacted,
            SUM(CASE WHEN status = 'Converted' THEN 1 ELSE 0 END) as converted,
            SUM(CASE WHEN status = 'Rejected' THEN 1 ELSE 0 END) as rejected
        FROM contact_messages
        """
        return self.db.execute_query(query, fetch_one=True)
