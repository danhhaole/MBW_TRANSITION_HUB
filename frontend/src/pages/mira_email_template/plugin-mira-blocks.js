export default function pluginMIRABlocks(editor) {
    const bm = editor.BlockManager;

    // JSON-like templates provided by app configuration
    const blocks = [
    // 1. EMAIL KÍCH HOẠT: Sau khi điền Form Landing Page (Trigger)
    {
      "template_id": "EMAIL-JF-WELCOME-001",
      "template_name": "Email Chào mừng Job Fair & Mời Tải CV",
      "name": "Email Chào mừng Job Fair & Mời Tải CV",
      "subject": "Cảm ơn bạn, {{candidate_name}}! Cơ hội nghề nghiệp tại XYZ đang chờ bạn!",
      "template_type": "other-email",
      "status": "Active",
      "is_active": 1,
      "auto_send": 0,
      "default_template": 1,
      "category": "Activation/Conversion",
      "sender_profile": {
        "sender_name": "Đội ngũ Tuyển dụng XYZ",
        "sender_email": "tuyendung@company.com"
      },
      "content": {
        "body_html": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Chào mừng Job Fair & Mời Tải CV</h2>
            <p>Chào bạn <strong>{{candidate_name}}</strong>,</p>
            <p>Công ty XYZ rất vui khi bạn đã ghé thăm gian hàng của chúng tôi! Để chúng tôi xem xét hồ sơ của bạn một cách nhanh chóng, hãy tải CV lên qua đường link dưới đây:</p>
            <p><a href="{{CV_UPLOAD_LINK}}" style="display:inline-block;background:#2563eb;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Tải CV Lên Ngay</a></p>
            <p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{CV_UPLOAD_LINK}}</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
        `,
        "body_plain_text": "Chào bạn {{candidate_name}}, cảm ơn bạn đã đăng ký. Vui lòng tải CV lên tại: {{CV_UPLOAD_LINK}}"
      },
      "html_content": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Chào mừng Job Fair & Mời Tải CV</h2>
            <p>Chào bạn <strong>{{candidate_name}}</strong>,</p>
            <p>Công ty XYZ rất vui khi bạn đã ghé thăm gian hàng của chúng tôi! Để chúng tôi xem xét hồ sơ của bạn một cách nhanh chóng, hãy tải CV lên qua đường link dưới đây:</p>
            <p><a href="{{CV_UPLOAD_LINK}}" style="display:inline-block;background:#2563eb;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Tải CV Lên Ngay</a></p>
            <p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{CV_UPLOAD_LINK}}</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
      `,
      "template_content": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Chào mừng Job Fair & Mời Tải CV</h2>
            <p>Chào bạn <strong>{{candidate_name}}</strong>,</p>
            <p>Công ty XYZ rất vui khi bạn đã ghé thăm gian hàng của chúng tôi! Để chúng tôi xem xét hồ sơ của bạn một cách nhanh chóng, hãy tải CV lên qua đường link dưới đây:</p>
            <p><a href="{{CV_UPLOAD_LINK}}" style="display:inline-block;background:#2563eb;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Tải CV Lên Ngay</a></p>
            <p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{CV_UPLOAD_LINK}}</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
      `,
      "message": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Chào mừng Job Fair & Mời Tải CV</h2>
            <p>Chào bạn <strong>{{candidate_name}}</strong>,</p>
            <p>Công ty XYZ rất vui khi bạn đã ghé thăm gian hàng của chúng tôi! Để chúng tôi xem xét hồ sơ của bạn một cách nhanh chóng, hãy tải CV lên qua đường link dưới đây:</p>
            <p><a href="{{CV_UPLOAD_LINK}}" style="display:inline-block;background:#2563eb;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Tải CV Lên Ngay</a></p>
            <p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{CV_UPLOAD_LINK}}</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
      `,
      "mjml_content": "",
      "css_content": `
/* Email Chào mừng Job Fair & Mời Tải CV */
table {
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
}
a {
  text-decoration: none;
}
h2 {
  margin: 0 0 20px 0;
  font-size: 24px;
  font-weight: bold;
  line-height: 1.4;
}
p {
  margin: 0 0 15px 0;
  font-size: 16px;
  line-height: 1.6;
}
      `,
      "personalization_config": {
        "candidate_fields": [{"variable_name": "candidate_name", "data_field": "full_name"}],
        "tracked_links": [{"variable_name": "CV_UPLOAD_LINK", "purpose": "CV Upload Form Access"}]
      }
    },


    // 2. EMAIL LÀM GIÀU DỮ LIỆU: Kêu gọi cập nhật Kỹ năng/Sở thích (Nếu chưa nộp CV)
    {
      "template_id": "EMAIL-ENRICH-SKILL-002",
      "template_name": "Nhắc nhở & Thu thập Kỹ năng thay thế",
      "name": "Nhắc nhở & Thu thập Kỹ năng thay thế",
      "subject": "Bạn có 2 phút không, {{candidate_name}}? Chia sẻ thêm về chuyên môn của bạn!",
      "template_type": "other-email",
      "status": "Active",
      "is_active": 1,
      "auto_send": 0,
      "default_template": 1,
      "category": "Data Enrichment/Nurturing",
      "sender_profile": {
        "sender_name": "Đội ngũ Tuyển dụng XYZ",
        "sender_email": "tuyendung@company.com"
      },
      "content": {
        "body_html": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Nhắc nhở & Thu thập Kỹ năng</h2>
            <p>Chúng tôi thấy bạn chưa kịp tải CV lên. Thay vì chờ đợi, bạn có thể dành 2 phút điền vào form ngắn này để chia sẻ về kỹ năng và sở thích.</p>
            <p><a href="{{SKILL_FORM_LINK}}" style="display:inline-block;background:#10b981;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Cập nhật Kỹ năng</a></p>
            <p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{SKILL_FORM_LINK}}</p>
            <p>Việc này giúp chúng tôi dễ dàng tìm thấy cơ hội phù hợp cho bạn!</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
        `,
        "body_plain_text": "Chúng tôi chưa nhận được CV của bạn. Vui lòng cập nhật kỹ năng tại: {{SKILL_FORM_LINK}}"
      },
      "html_content": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Nhắc nhở & Thu thập Kỹ năng</h2>
            <p>Chúng tôi thấy bạn chưa kịp tải CV lên. Thay vì chờ đợi, bạn có thể dành 2 phút điền vào form ngắn này để chia sẻ về kỹ năng và sở thích.</p>
            <p><a href="{{SKILL_FORM_LINK}}" style="display:inline-block;background:#10b981;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Cập nhật Kỹ năng</a></p>
            <p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{SKILL_FORM_LINK}}</p>
            <p>Việc này giúp chúng tôi dễ dàng tìm thấy cơ hội phù hợp cho bạn!</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
      `,
      "template_content": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Nhắc nhở & Thu thập Kỹ năng</h2>
            <p>Chúng tôi thấy bạn chưa kịp tải CV lên. Thay vì chờ đợi, bạn có thể dành 2 phút điền vào form ngắn này để chia sẻ về kỹ năng và sở thích.</p>
            <p><a href="{{SKILL_FORM_LINK}}" style="display:inline-block;background:#10b981;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Cập nhật Kỹ năng</a></p>
            <p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{SKILL_FORM_LINK}}</p>
            <p>Việc này giúp chúng tôi dễ dàng tìm thấy cơ hội phù hợp cho bạn!</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
      `,
      "message": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Nhắc nhở & Thu thập Kỹ năng</h2>
            <p>Chúng tôi thấy bạn chưa kịp tải CV lên. Thay vì chờ đợi, bạn có thể dành 2 phút điền vào form ngắn này để chia sẻ về kỹ năng và sở thích.</p>
            <p><a href="{{SKILL_FORM_LINK}}" style="display:inline-block;background:#10b981;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Cập nhật Kỹ năng</a></p>
            <p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{SKILL_FORM_LINK}}</p>
            <p>Việc này giúp chúng tôi dễ dàng tìm thấy cơ hội phù hợp cho bạn!</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
      `,
      "mjml_content": "",
      "css_content": `
/* Nhắc nhở & Thu thập Kỹ năng thay thế */
table {
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
}
a {
  text-decoration: none;
}
h2 {
  margin: 0 0 20px 0;
  font-size: 24px;
  font-weight: bold;
  line-height: 1.4;
}
p {
  margin: 0 0 15px 0;
  font-size: 16px;
  line-height: 1.6;
}
      `,
      "personalization_config": {
        "candidate_fields": [{"variable_name": "candidate_name", "data_field": "full_name"}],
        "tracked_links": [{"variable_name": "SKILL_FORM_LINK", "purpose": "Skill/Interest Enrichment Form Access"}]
      }
    },


    // 3. EMAIL LÀM GIÀU DỮ LIỆU: Đo lường Mức độ Quan tâm (Nếu đã tương tác với nội dung)
    {
      "template_id": "EMAIL-ENGAGE-LEVEL-003",
      "template_name": "Đo lường Mức độ Quan tâm (Scoring)",
      "name": "Đo lường Mức độ Quan tâm (Scoring)",
      "subject": "{{candidate_name}}, bạn nghĩ sao về cơ hội tại XYZ?",
      "template_type": "other-email",
      "status": "Active",
      "is_active": 1,
      "auto_send": 0,
      "default_template": 1,
      "category": "Engagement/Scoring",
      "sender_profile": {
        "sender_name": "Đội ngũ Tuyển dụng XYZ",
        "sender_email": "tuyendung@company.com"
      },
      "content": {
        "body_html": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Đo lường Mức độ Quan tâm</h2>
            <p>Chúng tôi thấy bạn đã xem một số thông tin gần đây của XYZ. Để hiểu rõ hơn về kỳ vọng của bạn, hãy giúp chúng tôi đánh giá mức độ quan tâm của bạn qua khảo sát ngắn (chỉ 30 giây).</p>
            <p><a href="{{INTEREST_FORM_LINK}}" style="display:inline-block;background:#f59e0b;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Đánh giá Mức độ Quan tâm</a></p>
            <p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{INTEREST_FORM_LINK}}</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
        `,
        "body_plain_text": "Hãy đánh giá mức độ quan tâm của bạn qua form này: {{INTEREST_FORM_LINK}}"
      },
      "html_content": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Đo lường Mức độ Quan tâm</h2>
            <p>Chúng tôi thấy bạn đã xem một số thông tin gần đây của XYZ. Để hiểu rõ hơn về kỳ vọng của bạn, hãy giúp chúng tôi đánh giá mức độ quan tâm của bạn qua khảo sát ngắn (chỉ 30 giây).</p>
            <p><a href="{{INTEREST_FORM_LINK}}" style="display:inline-block;background:#f59e0b;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Đánh giá Mức độ Quan tâm</a></p>
            <p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{INTEREST_FORM_LINK}}</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
      `,
      "template_content": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Đo lường Mức độ Quan tâm</h2>
            <p>Chúng tôi thấy bạn đã xem một số thông tin gần đây của XYZ. Để hiểu rõ hơn về kỳ vọng của bạn, hãy giúp chúng tôi đánh giá mức độ quan tâm của bạn qua khảo sát ngắn (chỉ 30 giây).</p>
            <p><a href="{{INTEREST_FORM_LINK}}" style="display:inline-block;background:#f59e0b;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Đánh giá Mức độ Quan tâm</a></p>
            <p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{INTEREST_FORM_LINK}}</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
      `,
      "message": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Đo lường Mức độ Quan tâm</h2>
            <p>Chúng tôi thấy bạn đã xem một số thông tin gần đây của XYZ. Để hiểu rõ hơn về kỳ vọng của bạn, hãy giúp chúng tôi đánh giá mức độ quan tâm của bạn qua khảo sát ngắn (chỉ 30 giây).</p>
            <p><a href="{{INTEREST_FORM_LINK}}" style="display:inline-block;background:#f59e0b;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:6px;">Đánh giá Mức độ Quan tâm</a></p>
            <p style="color:#6b7280;font-size:13px;">Nếu nút không hiển thị, hãy copy link sau vào trình duyệt: {{INTEREST_FORM_LINK}}</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
      `,
      "mjml_content": "",
      "css_content": `
/* Đo lường Mức độ Quan tâm (Scoring) */
table {
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
}
a {
  text-decoration: none;
}
h2 {
  margin: 0 0 20px 0;
  font-size: 24px;
  font-weight: bold;
  line-height: 1.4;
}
p {
  margin: 0 0 15px 0;
  font-size: 16px;
  line-height: 1.6;
}
      `,
      "personalization_config": {
        "candidate_fields": [{"variable_name": "candidate_name", "data_field": "full_name"}],
        "tracked_links": [{"variable_name": "INTEREST_FORM_LINK", "purpose": "Interest Level Scoring Form Access"}]
      }
    },


    // 4. EMAIL PHẢN HỒI TỰ ĐỘNG: Xác nhận hoàn tất hành động
    {
      "template_id": "EMAIL-SUCCESS-CONFIRM-004",
      "template_name": "Xác nhận Tải CV/Hoàn thành Form thành công",
      "name": "Xác nhận Tải CV/Hoàn thành Form thành công",
      "subject": "Thành công! Hồ sơ của bạn đã sẵn sàng tại hệ thống CRM của XYZ.",
      "template_type": "other-email",
      "status": "Active",
      "is_active": 1,
      "auto_send": 0,
      "default_template": 1,
      "category": "Confirmation",
      "sender_profile": {
        "sender_name": "Đội ngũ Tuyển dụng XYZ",
        "sender_email": "tuyendung@company.com"
      },
      "content": {
        "body_html": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Xác nhận Hoàn tất</h2>
            <p><strong>{{candidate_name}}</strong> thân mến,</p>
            <p>Hồ sơ/CV của bạn đã được tải lên/cập nhật thành công. Đội ngũ tuyển dụng của chúng tôi đang xem xét. Chúng tôi sẽ liên hệ với bạn trong vòng X ngày làm việc.</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
        `,
        "body_plain_text": "Hồ sơ của bạn đã được cập nhật thành công. Chúng tôi sẽ liên hệ trong X ngày làm việc."
      },
      "html_content": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Xác nhận Hoàn tất</h2>
            <p><strong>{{candidate_name}}</strong> thân mến,</p>
            <p>Hồ sơ/CV của bạn đã được tải lên/cập nhật thành công. Đội ngũ tuyển dụng của chúng tôi đang xem xét. Chúng tôi sẽ liên hệ với bạn trong vòng X ngày làm việc.</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
      `,
      "template_content": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Xác nhận Hoàn tất</h2>
            <p><strong>{{candidate_name}}</strong> thân mến,</p>
            <p>Hồ sơ/CV của bạn đã được tải lên/cập nhật thành công. Đội ngũ tuyển dụng của chúng tôi đang xem xét. Chúng tôi sẽ liên hệ với bạn trong vòng X ngày làm việc.</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
      `,
      "message": `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Xác nhận Hoàn tất</h2>
            <p><strong>{{candidate_name}}</strong> thân mến,</p>
            <p>Hồ sơ/CV của bạn đã được tải lên/cập nhật thành công. Đội ngũ tuyển dụng của chúng tôi đang xem xét. Chúng tôi sẽ liên hệ với bạn trong vòng X ngày làm việc.</p>
            <p>Trân trọng,<br>Đội ngũ Tuyển dụng XYZ</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>
      `,
      "mjml_content": "",
      "css_content": `
/* Xác nhận Tải CV/Hoàn thành Form thành công */
table {
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
}
a {
  text-decoration: none;
}
h2 {
  margin: 0 0 20px 0;
  font-size: 24px;
  font-weight: bold;
  line-height: 1.4;
}
p {
  margin: 0 0 15px 0;
  font-size: 16px;
  line-height: 1.6;
}
strong {
  font-weight: bold;
}
      `,
      "personalization_config": {
        "candidate_fields": [{"variable_name": "candidate_name", "data_field": "full_name"}],
        "tracked_links": []
      }
    }
    ];

    // Map JSON schema -> GrapesJS Block definitions
    blocks.forEach((tpl) => {
      const id = tpl.template_id;
      const label = tpl.name || tpl.template_id;
      // Use per-template body_html directly so each block controls its own layout/styles
      const htmlContent = (tpl.content && tpl.content.body_html) ? tpl.content.body_html : '';

      bm.add(id, {
        label,
        category: { id: 'MIRA', label: 'MIRA' },
        content: htmlContent,
      });
    });

    // Open MIRA category by default
    const cat = bm.getCategories().filter((c) => c.get('id') === 'MIRA')[0];
    if (cat) cat.set('open', true);
  }