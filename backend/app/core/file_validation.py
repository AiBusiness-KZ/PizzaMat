"""
File validation utilities
Secure file upload validation
"""

from fastapi import UploadFile, HTTPException, status
from typing import List, Optional
import os
import imghdr
from pathlib import Path

from app.config import settings


class FileValidator:
    """File validation for uploads"""
    
    ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
    ALLOWED_IMAGE_MIMETYPES = {
        'image/jpeg', 'image/png', 'image/webp', 'image/gif'
    }
    
    # Magic bytes for image formats
    IMAGE_SIGNATURES = {
        'jpeg': [b'\xFF\xD8\xFF'],
        'png': [b'\x89PNG\r\n\x1a\n'],
        'gif': [b'GIF87a', b'GIF89a'],
        'webp': [b'RIFF', b'WEBP'],
    }
    
    @staticmethod
    async def validate_image(
        file: UploadFile,
        max_size: int = None,
        allowed_extensions: List[str] = None
    ) -> bool:
        """
        Validate uploaded image file
        
        Args:
            file: Uploaded file
            max_size: Maximum file size in bytes
            allowed_extensions: List of allowed extensions
            
        Returns:
            True if file is valid
            
        Raises:
            HTTPException: If validation fails
        """
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        
        # Check filename
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required"
            )
        
        # Get file extension
        ext = os.path.splitext(file.filename)[1].lower()
        
        # Check extension
        allowed_exts = allowed_extensions or FileValidator.ALLOWED_IMAGE_EXTENSIONS
        if ext not in allowed_exts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File extension {ext} not allowed. Allowed: {', '.join(allowed_exts)}"
            )
        
        # Check content type
        if file.content_type not in FileValidator.ALLOWED_IMAGE_MIMETYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid content type: {file.content_type}"
            )
        
        # Read file content for validation
        content = await file.read()
        
        # Check file size
        file_size = len(content)
        max_allowed_size = max_size or settings.MAX_FILE_SIZE
        
        if file_size > max_allowed_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Max size: {max_allowed_size / 1024 / 1024:.1f}MB"
            )
        
        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file not allowed"
            )
        
        # Verify file signature (magic bytes)
        if not FileValidator._verify_image_signature(content):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file. File content doesn't match image format."
            )
        
        # Reset file pointer for later use
        await file.seek(0)
        
        return True
    
    @staticmethod
    def _verify_image_signature(content: bytes) -> bool:
        """
        Verify file is actually an image by checking magic bytes
        
        Args:
            content: File content bytes
            
        Returns:
            True if file signature matches known image formats
        """
        if len(content) < 12:
            return False
        
        # Check JPEG
        if content.startswith(b'\xFF\xD8\xFF'):
            return True
        
        # Check PNG
        if content.startswith(b'\x89PNG\r\n\x1a\n'):
            return True
        
        # Check GIF
        if content.startswith(b'GIF87a') or content.startswith(b'GIF89a'):
            return True
        
        # Check WebP (RIFF + WEBP)
        if content.startswith(b'RIFF') and b'WEBP' in content[:12]:
            return True
        
        return False
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent path traversal
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Get just the filename, no path
        filename = os.path.basename(filename)
        
        # Remove any dangerous characters
        filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-', '.'))
        
        # Limit length
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[:255 - len(ext)] + ext
        
        return filename


async def validate_upload_image(file: UploadFile) -> bool:
    """
    Convenience function to validate image upload
    
    Usage:
        await validate_upload_image(file)
    """
    return await FileValidator.validate_image(file)
