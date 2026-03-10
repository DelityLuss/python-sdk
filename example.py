from src.multi_upload_tool import MultiUploadClient

def main():
    client = MultiUploadClient(api_token="your_api_token_here")
    
    # Just checking structure
    print(f"Client initialized with base url: {client.base_url}")

    print()
    print("#==================================================")
    print("# Account Resource")
    print("#==================================================")
    print()

    # List all connection accounts
    accounts = client.accounts.list()
    print(f"Total accounts: {len(accounts)}")

    # Get details of the first account if exists
    if accounts:
        first_account_id = accounts[0]['id']
        account_details = client.accounts.get(first_account_id)
        print(f"First account details: {account_details}")

    print()
    print("#==================================================")
    print("# WhiteLabel Resource")
    print("#==================================================")
    print()
    # List white label links
    whitelabel_links = client.whitelabel.list()
    print(f"Total white label links: {len(whitelabel_links)}")

    # Create a new white label link
    new_link = client.whitelabel.create(
        platform="tiktok",
        expires_in_hours=48,
        logoUrl="https://example.com/logo.png",
        title="My White Label Link",
        redirectUrl="https://example.com/redirect",
        tags=["marketing", "social"]
    )
    print(f"Created white label link: {new_link}")

    # Delete the created white label link
    deleted_link = client.whitelabel.delete(new_link['id'])
    print(f"Deleted white label link response: {deleted_link}")

    print()
    print("#==================================================")
    print("# ShortLink Resource")
    print("#==================================================")
    print()

    # List short links
    short_links = client.short_links.list()
    print(f"Total short links: {len(short_links)}")

    # Create a new short link
    new_short_link = client.short_links.create(
        url="https://google.com",
        # custom_alias="mycustomlink" # Nothing it will generate automatically   
    )

    # Create a new short link with custom rule
    new_short_link_custom = client.short_links.create(
        url="https://google.com",
        # custom_alias="mycustomlink12345"
        title="Google Link",
        description="A short link to Google",
        useDeepLinking=True,
        botProtection=True,
        safe_page="https://example.com/safe",
        rules=[
            {
                "type": "geo",
                "destination": "https://global.google.com",
                "countryCodes": "US",
                "priority": 1
            },
            {
                "type": "device",
                "devices": "mobile",
                "destination": "https://m.google.com",
                "priority": 2
            }
        ]
    )

    print(f"Created short link: {new_short_link}")
    print(f"Created short link with custom rules: {new_short_link_custom}")

    # Update the created short link
    updated_short_link = client.short_links.update(
        new_short_link['id'],
        title="Updated Google Link",
        description="An updated short link to Google"
    )
    print(f"Updated short link: {updated_short_link}")


    # Get details of the created short link
    short_link_details = client.short_links.get(new_short_link['id'])
    print(f"Short link details: {short_link_details}")

    # Delete the created short link
    deleted_short_link = client.short_links.delete(new_short_link['id'])
    print(f"Deleted short link response: {deleted_short_link}")
    deleted_short_link_custom = client.short_links.delete(new_short_link_custom['id'])
    print(f"Deleted short link with custom rules response: {deleted_short_link_custom}")


    print()
    print("#==================================================")
    print("# Webhook Resource")
    print("#==================================================")
    print()

    # List webhooks
    webhooks = client.webhooks.list()
    print(f"Total webhooks: {len(webhooks)}")

    # Create a new webhook
    new_webhook = client.webhooks.create(
        url="https://example.com/webhook",
        events=["upload.completed", "account.connected"]
    )
    print(f"Created webhook: {new_webhook}")
    print(new_webhook)

    # test webhook
    test_response = client.webhooks.test(new_webhook['id'])
    print(f"Test webhook response: {test_response}")

    # Delete the created webhook
    deleted_webhook = client.webhooks.delete(new_webhook['id'])
    print(f"Deleted webhook response: {deleted_webhook}")


    print()
    print("#==================================================")
    print("# Team Resource")
    print("#==================================================")
    print()

    # List team members
    team_members = client.teams.list_members()
    print(f"Total team members: {len(team_members)}")

    # Invite a new member
    invited_member = client.teams.invite(
        # email="test@placeholder.com",
        role="MEMBER"
    )
    print(f"Invited team member: {invited_member}")

    # Update member role
    if team_members:
        member_id = team_members[0]['id']
        updated_member = client.teams.update_member_role(
            member_id=member_id,
            role="ADMIN",
            isActive=True
        )
        print(f"Updated team member: {updated_member}")

        # Remove member
        removed_member = client.teams.remove_member(member_id)
        print(f"Removed team member response: {removed_member}")

    print()
    print("#==================================================")
    print("# Upload Resource")
    print("#==================================================")
    print()

    # List uploads
    uploads = client.uploads.list()
    print(f"Total uploads: {len(uploads)}")

    # Get details of the first upload if exists
    if uploads:
        first_upload_id = uploads[0]['id']
        upload_details = client.uploads.get(first_upload_id)
        print(f"First upload details: {upload_details}")

    
    # Update upload details (only schedule upload)
        updated_upload = client.uploads.update(
            first_upload_id,
            title="Updated Upload Title",
            description="Updated description for the upload",
            scheduledFor="2024-12-31T12:00:00Z"
        )
        print(f"Updated upload details: {updated_upload}")  


    # Get upload limits for the first account
    if accounts:
        upload_limit = client.uploads.limits(accounts[0]['id'])
        print(f"Upload limit details: {upload_limit}")

    # Upload a video to TikTok
    if True:
        first_account_id = 37
        # Example 1: Upload TikTok Video with file path
        print("\n--- TikTok Video Upload (with file path) ---")
        video_upload = client.uploads.upload(
            account_id=first_account_id,
            file_path="/path/to/video.mp4",
            title="Check out this amazing video! 🎬 #FYP #ForYouPage",
            description="This is a test video upload",
            # schedule_date="2025-02-15T10:00:00Z",
            privacy_level="PUBLIC_TO_EVERYONE",
            disable_comment=False,
            disable_duet=False,
            disable_stitch=False,
            brand_content_toggle=False,
            is_aigc=False,
            post_mode="DIRECT_POST",
        )
        print(f"Video upload response: {video_upload}")

        # Example 1b: Upload TikTok Video with binary file object
        print("\n--- TikTok Video Upload (with file object) ---")
        with open("/path/to/another_video.mp4", "rb") as video_file:
            video_upload_binary = client.uploads.upload(
                account_id=first_account_id,
                file_path=video_file,  # Pass file object directly
                title="Another amazing video! 🎥",
                privacy_level="SELF_ONLY",
                post_mode="DRAFT"
            )
            print(f"Video upload response: {video_upload_binary}")


        # Example 2: Upload TikTok Carousel with MULTIPLE photos in ONE request
        print("\n--- TikTok Carousel Upload (Multiple photos in one request) ---")
        carousel_upload = client.uploads.upload(
            account_id=first_account_id,
            file_path=[
                "/path/to/photo1.jpg",
                "/path/to/photo2.jpg",
                "/path/to/photo3.jpg"
            ],
            title="My photo dump 📸",
            description="Beautiful moments from my day",
            media_type="IMAGE",
            schedule_date="2025-02-16T14:30:00Z",
            privacy_level="PUBLIC_TO_EVERYONE",
            auto_add_music=True,
            photo_cover_index=1,
            post_mode="DRAFT"
        )
        print(f"Carousel upload response: {carousel_upload}")

        # Example 2b: Upload TikTok Carousel with file objects (in one request)
        print("\n--- TikTok Carousel Upload (with file objects) ---")
        with open("/path/to/photo1.jpg", "rb") as photo1, \
             open("/path/to/photo2.jpg", "rb") as photo2, \
             open("/path/to/photo3.jpg", "rb") as photo3:
            carousel_upload_binary = client.uploads.upload(
                account_id=first_account_id,
                file_path=[photo1, photo2, photo3],
                title="Another photo carousel! 🖼️",
                media_type="IMAGE",
                auto_add_music=True,
                post_mode="DRAFT"
            )
            print(f"Carousel upload response: {carousel_upload_binary}")


if __name__ == "__main__":
    main()
