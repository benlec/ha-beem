# Brand Images for Beem Solar Integration

For Home Assistant custom integrations, you need to provide brand images in specific locations and formats. Here are the requirements:

## Image Locations and Names

1. Create a `brands` directory in your integration folder:
   ```
   custom_components/beem/brands/
   ```

2. Inside the brands directory, you need to create two subdirectories:
   ```
   custom_components/beem/brands/icon/
   custom_components/beem/brands/logo/
   ```

## Required Images

1. **Icon** (`icon.png`):
   - Location: `custom_components/beem/brands/icon/icon.png`
   - Requirements:
     - PNG format
     - Square dimensions (256x256 pixels recommended)
     - Should work well on both light and dark backgrounds
     - Should be recognizable at smaller sizes

2. **Logo** (`logo.png`):
   - Location: `custom_components/beem/brands/logo/logo.png`
   - Requirements:
     - PNG format
     - Rectangular format, landscape orientation recommended
     - Minimum width: 256 pixels
     - Should work well on both light and dark backgrounds

## Image Usage
- The icon will be used in the integrations page and other places where a small identifier is needed
- The logo will be used on the integration details/setup page and other places where brand identification is important

## Best Practices
- Use transparent backgrounds for both images
- Ensure images are optimized for web use
- Test how the images look on both light and dark themes
- Keep file sizes reasonable (under 100KB each is recommended)

To implement this:
1. Create the directory structure mentioned above
2. Place your icon.png in the icon directory
3. Place your logo.png in the logo directory
4. The images will be automatically picked up by Home Assistant when the integration loads