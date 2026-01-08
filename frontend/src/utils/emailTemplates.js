/**
 * Default email template utility functions
 * Centralized location for default email template HTML and CSS
 */

/**
 * Get default email template HTML
 * @returns {string} Default email template HTML string
 */
export const getDefaultEmailTemplate = () => {
  return `
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="font-family: Arial, sans-serif;">
            <tr>
                <td style="background-color: #f4f4f4; padding: 20px;">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="margin: 0 auto; background: #ffffff;">
                        <!-- Header -->
                        <tr>
                            <td style="background-color: #ffffff; padding: 30px 20px; text-align: center;">
                                <h1 style="margin: 0; color: #333333; font-size: 28px; font-weight: bold;">Welcome to Our Campaigns</h1>
                            </td>
                        </tr>
                        
                        <!-- Main Content -->
                        <tr>
                            <td style="padding: 30px 20px;">
                                <p style="margin: 0 0 15px 0; font-size: 16px; line-height: 1.5; color: #333333;">Dear {{ full_name }},</p>
                                <p style="margin: 0 0 15px 0; font-size: 16px; line-height: 1.5; color: #333333;">Thank you for your application for the position. We have received your application and will review it carefully.</p>
                                <p style="margin: 0 0 25px 0; font-size: 16px; line-height: 1.5; color: #333333;">We will contact you within 5-7 business days regarding the next steps in our hiring process.</p>
                                
                                <!-- Button -->
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto;">
                                    <tr>
                                        <td style="background-color: #007bff; border-radius: 4px;">
                                            <a href="#" style="background-color: #007bff; border: none; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; font-size: 16px;">
                                                View Application Status
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Signature -->
                        <tr>
                            <td style="padding: 20px; font-size: 16px; line-height: 1.5; color: #333333;">
                                <p style="margin: 0 0 10px 0;">Best regards,</p>
                                <p style="margin: 0; font-weight: bold;">HR Team</p>

                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #343a40; color: white; padding: 30px 20px; text-align: center;">
                                <p style="margin: 0 0 10px 0; font-size: 14px;">© 2025 MBW Transition Hub. All rights reserved.</p>
                                <p style="margin: 0; font-size: 12px;">
                                    <a href="#" style="color: #adb5bd; text-decoration: none;">Unsubscribe</a> | 
                                    <a href="#" style="color: #adb5bd; text-decoration: none;">Privacy Policy</a>
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    `;
};

/**
 * Get default email template CSS
 * @returns {string} Default email template CSS string
 */
export const getDefaultEmailTemplateCss = () => {
  return `
    body { margin: 0; padding: 0; background-color: #f4f4f4; }
    table { border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
    td { padding: 0; vertical-align: top; }
    p { margin: 0; padding: 0; }
    h1, h2, h3, h4, h5, h6 { margin: 0; padding: 0; }
    a { text-decoration: none; }
    .button { display: inline-block; background-color: #007bff; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 4px; }
    * { box-sizing: border-box; }
    img { border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; }
    table { border-collapse: collapse !important; }
    body { height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }
    @media screen and (max-width: 600px) {
      .email-container { width: 100% !important; max-width: 100% !important; }
      .desktop-padding { padding-left: 20px !important; padding-right: 20px !important; }
    }
  `;
};

