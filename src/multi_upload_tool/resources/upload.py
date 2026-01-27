import json
from typing import List, Dict, Any, Optional, Union
from io import BytesIO
from .base import Resource

class UploadResource(Resource):
    def list(self, page: int = 1, limit: int = 100, platform: Optional[str] = None, 
             status: Optional[str] = None, search: Optional[str] = None) -> Dict[str, Any]:
        """
        List uploads with pagination and filtering.
        """
        params = {"page": page, "limit": limit}
        if platform: params['platform'] = platform
        if status: params['status'] = status
        if search: params['search'] = search
        
        return self.client.request("GET", "/uploads", params=params).get("data", [])

    def get(self, upload_id: int) -> Dict[str, Any]:
        """Get upload details."""
        return self.client.request("GET", f"/uploads/{upload_id}").get("data", {})
    
    def update(self, upload_id: int, **kwargs) -> Dict[str, Any]:
        """Update upload details."""
        data = {}
        if 'title' in kwargs: data['title'] = kwargs['title'] 
        if 'description' in kwargs: data['description'] = kwargs['description']
        if 'scheduledFor' in kwargs: data['scheduledFor'] = kwargs['scheduledFor']
        return self.client.request("PUT", f"/uploads/{upload_id}", json=data).get("data", {})
    
    def limit(self) -> Dict[str, Any]:
        """Update upload limit."""
        return self.client.request("PUT", f"/limits").get("data", {})

    def _upload_file(self, account_id: Union[str, int], 
                     files: Dict[str, Any], data: Dict[str, Any],
                     params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Internal helper for file uploads."""
        # Platform is determined by accountId on the server side
        data['accountId'] = str(account_id)
        
        try:
            return self.client.request("POST", "/upload", data=data, files=files, params=params)
        finally:
            # Close all opened files to prevent resource leaks
            for field_files in files.values():
                if isinstance(field_files, list):
                    for f in field_files:
                        if hasattr(f, 'close'):
                            try:
                                f.close()
                            except:
                                pass
                else:
                    if hasattr(field_files, 'close'):
                        try:
                            field_files.close()
                        except:
                            pass

    def upload(self, account_id: Union[str, int, List[Union[str, int]]], 
               file_path: Optional[Union[str, Any, List[Union[str, Any]]]] = None, 
               async_mode: bool = True, **kwargs) -> Dict[str, Any]:
        """
        Unified upload function for all platforms and Bulk uploads.

        Args:
            account_id: Account ID (str/int) or List of IDs for bulk upload.
            file_path: Path to the media file (str), file-like object, or List of paths/objects for carousel.
                       For carousels, pass a list: ["/path/to/photo1.jpg", "/path/to/photo2.jpg", ...]
            async_mode: Default `True`. If `False`, the API waits for upload completion.
            **kwargs: Platform-specific parameters. Common ones:
                - title, description, schedule_date
                - YouTube: privacy_status, tags, category_id, thumbnail_path, etc.
        """
        # Prepare query parameters
        params = {}
        if not async_mode:
            params['async'] = 'false'
        
        # Handle Bulk Upload
        if isinstance(account_id, list):
            field_name = 'video'
            if kwargs.get('media_type') == 'IMAGE':
                field_name = 'photo'
            
            files = {}
            if file_path:
                if isinstance(file_path, str):
                    with open(file_path, 'rb') as f:
                        files[field_name] = BytesIO(f.read())
                else:
                    # file_path is already a file-like object
                    if hasattr(file_path, 'read'):
                        files[field_name] = BytesIO(file_path.read())
                    else:
                        files[field_name] = file_path
            
            data = {'accounts': json.dumps(account_id)}
            data.update(kwargs)
            return self.client.request("POST", "/upload/bulk", data=data, files=files)

        # Handle Single Upload
        files = {}
        data = kwargs.copy()
        
        # Handle carousel: List of files
        if isinstance(file_path, list):
            # Multiple files for carousel
            media_type = data.get('media_type')
            is_image = False
            
            if media_type == 'IMAGE':
                is_image = True
            elif not media_type and file_path and isinstance(file_path[0], str):
                ext = file_path[0].lower().split('.')[-1] if '.' in file_path[0] else ''
                if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                    is_image = True
            
            field_name = 'photo' if is_image else 'video'
            files[field_name] = []
            
            # Add all files to the list
            for fp in file_path:
                if isinstance(fp, str):
                    with open(fp, 'rb') as f:
                        files[field_name].append(BytesIO(f.read()))
                else:
                    # fp is already a file-like object
                    if hasattr(fp, 'read'):
                        files[field_name].append(BytesIO(fp.read()))
                    else:
                        files[field_name].append(fp)
        
        # Handle single file
        elif file_path:
            # Guess field name based on extension or media_type arg
            media_type = data.get('media_type')
            is_image = False
            
            if media_type == 'IMAGE':
                is_image = True
            elif not media_type and isinstance(file_path, str):
                # Only check extension if file_path is a string
                ext = file_path.lower().split('.')[-1] if '.' in file_path else ''
                if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                    is_image = True
            
            field_name = 'photo' if is_image else 'video'
            
            # Support both file path (str) and file-like objects
            if isinstance(file_path, str):
                with open(file_path, 'rb') as f:
                    files[field_name] = BytesIO(f.read())
            else:
                # file_path is already a file-like object
                if hasattr(file_path, 'read'):
                    files[field_name] = BytesIO(file_path.read())
                else:
                    files[field_name] = file_path
            
        # Handle optional thumbnail path if provided for convenience
        if 'thumbnail_path' in data:
             with open(data.pop('thumbnail_path'), 'rb') as f:
                 files['thumbnail'] = BytesIO(f.read())
        
        # Handle tags list to string conversion if needed
        if 'tags' in data and isinstance(data['tags'], list):
             data['tags'] = ",".join(data['tags'])

        return self._upload_file(account_id, files, data, params=params)
