from fastmcp import Client
import unittest
import asyncio
from datetime import datetime

class TestGmailMCP(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Initialize the MCP client before each test"""
        self.client = Client("http://localhost:8000/api/mcp")  # Point to the MCP endpoint
        self.test_email = "recoverynthu2@gmail.com"  # Your test email

    async def test_send_email(self):
        """Test sending an email"""
        async with self.client:
            response = await self.client.call_tool("send_email", {
                "to": self.test_email,
                "subject": "Test Email from MCP",
                "body": "This is a test email sent via Gmail MCP"
            })
            result = response.data
            self.assertIn('messageId', result)
            self.message_id = result['messageId']  # Save for other tests
            print('Email sent with message ID:', self.message_id)

    async def test_read_email(self):
        """Test reading an email"""
        async with self.client:
            # First send an email to ensure we have one to read
            send_response = await self.client.call_tool("send_email", {
                "to": self.test_email,
                "subject": "Email to Read",
                "body": "This email will be read via MCP"
            })
            message_id = send_response.data['messageId']

            # Now read the email
            read_response = await self.client.call_tool("read_email", {
                "message_id": message_id
            })
            result = read_response.data
            self.assertEqual(result['subject'], "Email to Read")

    async def test_search_emails(self):
        """Test searching emails"""
        async with self.client:
            response = await self.client.call_tool("search_emails", {
                "query": "test",
                "max_results": 5,
                "include_content": True
            })
            result = response.data
            print("Search response:", result)
            self.assertIn('messages', result)
        

    async def test_filter_emails(self):
        """Test filtering emails"""
        async with self.client:
            response = await self.client.call_tool("filter_emails", {
                "query": "test",
                "from_email": self.test_email,
                "max_results": 5
            })
            result = response.data
            self.assertIn('count', result)
            self.assertIn('messages', result)
            print('we got some results:', result)

    async def test_unread_emails(self):
        """Test getting unread emails"""
        async with self.client:
            response = await self.client.call_tool("get_unread_emails", {
                "max_results": 5
            })
            result = response.data
            self.assertIn('unread_count', result)
            self.assertIn('messages', result)
            print('Unread emails:', result)

# Simple test without unittest
async def test_simple():
    """Simple test without unittest framework"""
    client = Client("http://localhost:8000/api/mcp")
    
    async with client:
        # Test sending an email
        print("Testing send email...")
        response = await client.call_tool("send_email", {
            "to": "recoverynthu2@gmail.com",
            "subject": "Test MCP",
            "body": "Testing the Gmail MCP"
        })
        print("Send response:", response.data)
        
        # Test getting unread emails
        print("\nTesting get unread emails...")
        unread = await client.call_tool("get_unread_emails", {
            "max_results": 5
        })
        print("Unread emails:", unread.data)

if __name__ == '__main__':
    # You can either run the unittest suite
    print("Running unittest suite...")
    unittest.main()
    
    # Or run the simple test
    # print("Running simple test...")
    # asyncio.run(test_simple())