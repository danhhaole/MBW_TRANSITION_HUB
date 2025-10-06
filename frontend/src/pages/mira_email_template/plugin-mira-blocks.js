export default function pluginMIRABlocks(editor) {
    const bm = editor.BlockManager;
  
    const blocks = [
      
      {
        id: 'mira-invite-interview',
        label: '📨 Mời phỏng vấn',
        category: 'Email Templates',
        content: `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333333;">
          <tr><td>
            <h2 style="color:#1a1a1a;">Thư Mời Tham Dự Phỏng Vấn</h2>
            <p>Gửi <strong>{{ can_full_name }}</strong>,</p>
            <p>Chúng tôi chân thành cảm ơn bạn vì đã quan tâm và nộp hồ sơ ứng tuyển vào vị trí <strong>{{ job_title }}</strong> tại <strong>{{ company_name }}</strong>.</p>
            <p>Sau quá trình xem xét kỹ lưỡng, chúng tôi rất ấn tượng với hồ sơ và những kinh nghiệm mà bạn đã chia sẻ. Vì vậy, chúng tôi trân trọng mời bạn tham dự buổi phỏng vấn để tìm hiểu rõ hơn về định hướng nghề nghiệp cũng như cơ hội hợp tác giữa hai bên.</p>
            <p><strong>Thông tin buổi phỏng vấn:</strong><br>
            🗓 <strong>Thời gian:</strong> {{ interview_time }}<br>
            📍 <strong>Địa điểm:</strong> {{ interview_location }}<br>
            💬 <strong>Hình thức:</strong> {{ interview_mode }}</p>
            <p>Chúng tôi rất mong chờ được gặp bạn.</p>
            <p>Trân trọng,<br>
            <strong>{{ full_name }}</strong><br>
            {{ position }}<br>
            {{ company_name }}</p>
          </td></tr>
        </table>
      </td>
    </tr>
  </table>`
      },
      {
        id: 'mira-offer-letter',
        label: '🎉 Nhận việc',
        category: 'Email Templates',
        content: `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333;">
        <tr><td>
          <h2>Thư Mời Nhận Việc</h2>
          <p>Gửi <strong>{{ can_full_name }}</strong>,</p>
          <p>Chúng tôi vui mừng thông báo rằng bạn đã vượt qua tất cả các vòng tuyển dụng tại <strong>{{ company_name }}</strong> cho vị trí <strong>{{ job_title }}</strong>.</p>
          <p>Chúng tôi tin tưởng rằng với kiến thức và kinh nghiệm của bạn, bạn sẽ đóng góp tích cực vào sự phát triển của đội ngũ chúng tôi.</p>
          <p><strong>Điều kiện làm việc dự kiến:</strong><br>
          📅 Ngày bắt đầu: {{ start_date }}<br>
          💼 Vị trí: {{ job_title }}<br>
          💰 Mức lương: {{ job_salary }}</p>
          <p>Chúng tôi rất mong được chào đón bạn gia nhập đội ngũ. Vui lòng xác nhận lại với chúng tôi trước ngày <strong>{{ confirm_deadline }}</strong>.</p>
          <p>Trân trọng,<br><strong>{{ sender_full_name }}</strong><br>{{ sender_position }}</p>
        </td></tr>
      </table>
    </td></tr>
  </table>`
      },
      {
        id: 'mira-thank-you',
        label: '🙏 Cảm ơn sau phỏng vấn',
        category: 'Email Templates',
        content: `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333;">
        <tr><td>
          <h2>Cảm Ơn Bạn Đã Dành Thời Gian Phỏng Vấn</h2>
          <p>Gửi <strong>{{ can_full_name }}</strong>,</p>
          <p>Chúng tôi trân trọng cảm ơn bạn đã dành thời gian tham gia buổi phỏng vấn tại {{ company_name }}. Qua cuộc trò chuyện, chúng tôi đánh giá cao sự chuyên nghiệp và đam mê của bạn.</p>
          <p>Hồ sơ của bạn sẽ được cân nhắc cẩn thận và chúng tôi sẽ phản hồi trong thời gian sớm nhất.</p>
          <p>Trân trọng,<br><strong>{{ full_name }}</strong></p>
        </td></tr>
      </table>
    </td></tr>
  </table>`
      },
      {
        id: 'mira-reject',
        label: '🙁 Từ chối ứng viên',
        category: 'Email Templates',
        content: `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333;">
        <tr><td>
          <h2>Phản Hồi Về Kết Quả Tuyển Dụng</h2>
          <p>Gửi <strong>{{ can_full_name }}</strong>,</p>
          <p>Sau quá trình xem xét kỹ lưỡng, chúng tôi rất tiếc phải thông báo rằng bạn chưa được chọn cho vị trí <strong>{{ job_title }}</strong> tại thời điểm này.</p>
          <p>Chúng tôi thực sự đánh giá cao những nỗ lực và sự quan tâm của bạn. Mong rằng chúng tôi sẽ có cơ hội hợp tác trong tương lai gần.</p>
          <p>Chúc bạn mọi điều tốt đẹp trong hành trình nghề nghiệp sắp tới.</p>
          <p>Trân trọng,<br><strong>{{ full_name }}</strong></p>
        </td></tr>
      </table>
    </td></tr>
  </table>`
      },
      {
        id: 'mira-send-test',
        label: '📝 Gửi bài test',
        category: 'Email Templates',
        content: `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333;">
        <tr><td>
          <h2>Yêu Cầu Làm Bài Kiểm Tra Đánh Giá</h2>
          <p>Gửi <strong>{{ can_full_name }}</strong>,</p>
          <p>Trong bước tiếp theo của quy trình tuyển dụng vị trí <strong>{{ job_public_title }}</strong>, chúng tôi xin gửi đến bạn bài kiểm tra chuyên môn để đánh giá thêm kỹ năng phù hợp với vị trí ứng tuyển.</p>
          <p><strong>Thông tin bài test:</strong><br>
          📎 Đường dẫn: {{ quiz_link }}<br>
          ⏰ Thời hạn: {{ deadline }}</p>
          <p>Vui lòng hoàn thành và gửi lại bài trước thời hạn trên.</p>
          <p>Chúc bạn hoàn thành tốt và hẹn gặp lại ở vòng tiếp theo.</p>
          <p>Trân trọng,<br><strong>{{ full_name }}</strong></p>
        </td></tr>
      </table>
    </td></tr>
  </table>`
      },
      {
        id: 'MIRA-onboarding',
        label: '🚀 Onboarding',
        category: 'Email Templates',
        content: `
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;padding:40px;border-radius:8px;font-family:'Segoe UI',sans-serif;box-shadow:0 2px 10px rgba(0,0,0,0.05);color:#333;">
        <tr><td>
          <h2>Chào Mừng Bạn Gia Nhập Đội Ngũ</h2>
          <p>Gửi <strong>{{ can_full_name }}</strong>,</p>
          <p>Chào mừng bạn đã chính thức trở thành thành viên của {{ company_name }}!</p>
          <p>Chúng tôi rất vui mừng được đồng hành cùng bạn trong chặng đường sắp tới. Trong thời gian tới, bộ phận nhân sự sẽ liên hệ để hướng dẫn các thủ tục cần thiết và cung cấp tài liệu giúp bạn nhanh chóng làm quen với công việc.</p>
          <p>Nếu bạn có bất kỳ câu hỏi nào, đừng ngần ngại liên hệ với chúng tôi.</p>
          <p>Trân trọng,<br><strong>{{ full_name }}</strong></p>
        </td></tr>
      </table>
    </td></tr>
  </table>`
      },{
        id: 'mira-email-layout',
        label: '🧱 Layout chuẩn Email',
        category: 'MIRA',
        content: `
          <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background-color:#f4f4f4;padding: 30px 0;">
            <tr>
              <td align="center">
                <table role="presentation" cellpadding="0" cellspacing="0" width="600" style="background:#ffffff;padding:40px;border-radius:6px;font-family:sans-serif;">
                  <tr>
                    <td>
                      <!-- Nội dung ở đây -->
                      <p>Xin chào <strong>{{ can_full_name }}</strong>,</p>
                      <p>Cảm ơn bạn đã ứng tuyển...</p>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        `
      },
      {
        id: 'mira-header',
        label: '👤 MIRA Header',
        category: 'MIRA',
        content: `
          <table style="width:100%;padding:20px;background:#f4f4f4;">
            <tr>
              <td style="font-size:20px;font-weight:bold;">{{ company_name }}</td>
              <td style="text-align:right;"><img src="{{ company_logo_url }}" height="40"/></td>
            </tr>
          </table>
        `
      },
      {
        id: 'mira-greeting',
        label: '👋 Lời chào',
        category: 'MIRA',
        content: `<p>Xin chào <strong>{{ candidate_name }}</strong>,</p>`
      },
      {
        id: 'mira-job-info',
        label: '📄 Thông tin công việc',
        category: 'MIRA',
        content: `
          <p>Bạn đã ứng tuyển vị trí <strong>{{ job_title }}</strong> tại <strong>{{ company_name }}</strong>.</p>
          <p>Lịch phỏng vấn: {{ interview_time }} tại {{ interview_location }}</p>
        `
      },
      {
        id: 'mira-cta-confirm',
        label: '✅ Button Xác nhận',
        category: 'MIRA',
        content: `
          <div style="text-align:center; margin:20px 0;">
            <a href="{{ confirm_url }}" style="background:#007bff;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">Xác nhận tham gia</a>
          </div>
        `
      },
      {
        id: 'mira-signature',
        label: '✍️ Chữ ký',
        category: 'MIRA',
        content: `
          <p>Trân trọng,</p>
          <p><strong>{{ sender_name }}</strong><br/>{{ sender_title }}<br/>{{ company_name }}</p>
        `
      },
      {
        id: 'mira-footer',
        label: '📩 Footer',
        category: 'MIRA',
        content: `
          <hr/>
          <p style="font-size:12px;color:gray;">
            Đây là email tự động, vui lòng không phản hồi. Nếu bạn có thắc mắc, hãy liên hệ <a href="mailto:{{ support_email }}">{{ support_email }}</a>.
          </p>
        `
      },
    ];
  
    blocks.forEach(block => bm.add(block.id, block));
  
    // Mở sẵn tab MIRA nếu có
    const cat = bm.getCategories().filter(c => c.get('id') === 'MIRA')[0];
    if (cat) cat.set('open', true);
  }
  