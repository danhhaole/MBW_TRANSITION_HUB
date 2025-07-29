// ladi-style-tailwind-blocks.js

export function loadLadiTailwindBlocks(editor) {
    const bm = editor.BlockManager;
    const st = editor.StyleManager;
  
    // 📦 BASIC BLOCKS

bm.add('1-column', {
    label: '1 Column',
    category: '📦 Basic',
    media: `<svg viewBox="0 0 24 24">
        <path fill="currentColor" d="M2 20h20V4H2v16Zm-1 0V4a1 1 0 0 1 1-1h20a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1Z"/>
      </svg>`,
    content: `
      <div class="p-4 bg-gray-100 rounded">Nội dung cột đơn</div>
    `
  });
  
  bm.add('2-columns', {
    label: '2 Columns',
    category: '📦 Basic',
    media: `<svg viewBox="0 0 23 24">
        <path fill="currentColor" d="M2 20h8V4H2v16Zm-1 0V4a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1ZM13 20h8V4h-8v16Zm-1 0V4a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1h-8a1 1 0 0 1-1-1Z"/>
      </svg>`,
    content: `
      <div class="grid grid-cols-2 gap-4">
        <div class="bg-gray-100 p-4 rounded">Cột 1</div>
        <div class="bg-gray-100 p-4 rounded">Cột 2</div>
      </div>
    `
  });
  
  bm.add('3-columns', {
    label: '3 Columns',
    category: '📦 Basic',
    media: `<svg viewBox="0 0 23 24">
        <path fill="currentColor" d="M2 20h4V4H2v16Zm-1 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1ZM17 20h4V4h-4v16Zm-1 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1ZM9.5 20h4V4h-4v16Zm-1 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1Z"/>
      </svg>`,
    content: `
      <div class="grid grid-cols-3 gap-4">
        <div class="bg-gray-100 p-4 rounded">Cột 1</div>
        <div class="bg-gray-100 p-4 rounded">Cột 2</div>
        <div class="bg-gray-100 p-4 rounded">Cột 3</div>
      </div>
    `
  });
  
  bm.add('2-columns-3-7', {
    label: '2 Columns 3/7',
    category: '📦 Basic',
    media: `<svg viewBox="0 0 24 24">
    <path fill="currentColor" d="M2 20h5V4H2v16Zm-1 0V4a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1ZM10 20h12V4H10v16Zm-1 0V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H10a1 1 0 0 1-1-1Z"/>
  </svg>`,
    content: `
      <div class="grid grid-cols-10 gap-4">
        <div class="col-span-3 bg-gray-100 p-4 rounded">3 phần</div>
        <div class="col-span-7 bg-gray-200 p-4 rounded">7 phần</div>
      </div>
    `
  });
  
  bm.add('text-block', {
    label: 'Text',
    category: '📦 Basic',
    media: `<svg viewBox="0 0 24 24">
    <path fill="currentColor" d="M18.5,4L19.66,8.35L18.7,8.61C18.25,7.74 17.79,6.87 17.26,6.43C16.73,6 16.11,6 15.5,6H13V16.5C13,17 13,17.5 13.33,17.75C13.67,18 14.33,18 15,18V19H9V18C9.67,18 10.33,18 10.67,17.75C11,17.5 11,17 11,16.5V6H8.5C7.89,6 7.27,6 6.74,6.43C6.21,6.87 5.75,7.74 5.3,8.61L4.34,8.35L5.5,4H18.5Z" />
  </svg>`,
    content: `<p class="text-gray-700">Văn bản đơn giản</p>`
  });
  
  bm.add('link-block', {
    label: 'Link',
    category: '📦 Basic',
    media: `<svg viewBox="0 0 24 24">
        <path fill="currentColor" d="M3.9,12C3.9,10.29 5.29,8.9 7,8.9H11V7H7A5,5 0 0,0 2,12A5,5 0 0,0 7,17H11V15.1H7C5.29,15.1 3.9,13.71 3.9,12M8,13H16V11H8V13M17,7H13V8.9H17C18.71,8.9 20.1,10.29 20.1,12C20.1,13.71 18.71,15.1 17,15.1H13V17H17A5,5 0 0,0 22,12A5,5 0 0,0 17,7Z" />
      </svg>`,
    content: `<a href="#" class="text-blue-600 underline">Liên kết mẫu</a>`
  });
  
  bm.add('image-block', {
    label: 'Image',
    category: '📦 Basic',
    media: `<svg viewBox="0 0 24 24">
        <path fill="currentColor" d="M21,3H3C2,3 1,4 1,5V19A2,2 0 0,0 3,21H21C22,21 23,20 23,19V5C23,4 22,3 21,3M5,17L8.5,12.5L11,15.5L14.5,11L19,17H5Z" />
      </svg>`,
    content: `<img src="https://via.placeholder.com/600x300" class="rounded w-full shadow" />`
  });
  
  bm.add('video-block', {
    label: 'Video',
    category: '📦 Basic',
    media: `<svg viewBox="0 0 24 24">
        <path fill="currentColor" d="M10,15L15.19,12L10,9V15M21.56,7.17C21.69,7.64 21.78,8.27 21.84,9.07C21.91,9.87 21.94,10.56 21.94,11.16L22,12C22,14.19 21.84,15.8 21.56,16.83C21.31,17.73 20.73,18.31 19.83,18.56C19.36,18.69 18.5,18.78 17.18,18.84C15.88,18.91 14.69,18.94 13.59,18.94L12,19C7.81,19 5.2,18.84 4.17,18.56C3.27,18.31 2.69,17.73 2.44,16.83C2.31,16.36 2.22,15.73 2.16,14.93C2.09,14.13 2.06,13.44 2.06,12.84L2,12C2,9.81 2.16,8.2 2.44,7.17C2.69,6.27 3.27,5.69 4.17,5.44C4.64,5.31 5.5,5.22 6.82,5.16C8.12,5.09 9.31,5.06 10.41,5.06L12,5C16.19,5 18.8,5.16 19.83,5.44C20.73,5.69 21.31,6.27 21.56,7.17Z" />
      </svg>`,
    content: `
      <div class="aspect-w-16 aspect-h-9">
        <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" 
                frameborder="0" allowfullscreen class="w-full h-full"></iframe>
      </div>
    `
  });
  
  bm.add('map-block', {
    label: 'Map',
    category: '📦 Basic',
    media: `<svg viewBox="0 0 24 24">
        <path fill="currentColor" d="M20.5,3L20.34,3.03L15,5.1L9,3L3.36,4.9C3.15,4.97 3,5.15 3,5.38V20.5A0.5,0.5 0 0,0 3.5,21L3.66,20.97L9,18.9L15,21L20.64,19.1C20.85,19.03 21,18.85 21,18.62V3.5A0.5,0.5 0 0,0 20.5,3M10,5.47L14,6.87V18.53L10,17.13V5.47M5,6.46L8,5.45V17.15L5,18.31V6.46M19,17.54L16,18.55V6.86L19,5.7V17.54Z" />
      </svg>`,
    content: `
      <iframe 
        class="w-full h-64 rounded"
        src="https://www.google.com/maps/embed?pb=!1m18..."
        frameborder="0" allowfullscreen></iframe>
    `
  });
  
  bm.add('link-box', {
    label: 'Link Block',
    category: '📦 Basic',
    media:`<svg viewBox="0 0 24 24">
      <path fill="currentColor" d="M3.9,12C3.9,10.29 5.29,8.9 7,8.9H11V7H7A5,5 0 0,0 2,12A5,5 0 0,0 7,17H11V15.1H7C5.29,15.1 3.9,13.71 3.9,12M8,13H16V11H8V13M17,7H13V8.9H17C18.71,8.9 20.1,10.29 20.1,12C20.1,13.71 18.71,15.1 17,15.1H13V17H17A5,5 0 0,0 22,12A5,5 0 0,0 17,7Z"></path>
    </svg>`,
    content: `
      <a href="#" class="block bg-blue-100 hover:bg-blue-200 p-4 rounded text-center">
        Click vào đây
      </a>
    `
  });
  
  bm.add('quote-block', {
    label: 'Quote',
    category: '📦 Basic',
    media:`<svg viewBox="0 0 24 24">
      <path fill="currentColor" d="M3.9,12C3.9,10.29 5.29,8.9 7,8.9H11V7H7A5,5 0 0,0 2,12A5,5 0 0,0 7,17H11V15.1H7C5.29,15.1 3.9,13.71 3.9,12M8,13H16V11H8V13M17,7H13V8.9H17C18.71,8.9 20.1,10.29 20.1,12C20.1,13.71 18.71,15.1 17,15.1H13V17H17A5,5 0 0,0 22,12A5,5 0 0,0 17,7Z"></path>
    </svg>`,
    content: `
      <blockquote class="border-l-4 border-gray-400 pl-4 italic text-gray-700">
        Đây là một trích dẫn từ khách hàng.
      </blockquote>
    `
  });
  
  bm.add('text-section', {
    label: 'Text section',
    category: '📦 Basic',
    media:`<svg viewBox="0 0 24 24">
        <path fill="currentColor" d="M21,6V8H3V6H21M3,18H12V16H3V18M3,13H21V11H3V13Z"></path>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 5.5c0-.3-.5-.5-1.3-.5H3.4c-.8 0-1.3.2-1.3.5v3c0 .3.5.5 1.3.5h17.4c.8 0 1.3-.2 1.3-.5v-3zM21 8H3V6h18v2zM22 10.5c0-.3-.5-.5-1.3-.5H3.4c-.8 0-1.3.2-1.3.5v3c0 .3.5.5 1.3.5h17.4c.8 0 1.3-.2 1.3-.5v-3zM21 13H3v-2h18v2z"></path><rect width="10" height="3" x="2" y="15" rx=".5"></rect></svg><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 5.5c0-.3-.5-.5-1.3-.5H3.4c-.8 0-1.3.2-1.3.5v3c0 .3.5.5 1.3.5h17.4c.8 0 1.3-.2 1.3-.5v-3zM21 8H3V6h18v2zM22 10.5c0-.3-.5-.5-1.3-.5H3.4c-.8 0-1.3.2-1.3.5v3c0 .3.5.5 1.3.5h17.4c.8 0 1.3-.2 1.3-.5v-3zM21 13H3v-2h18v2z"></path><rect width="10" height="3" x="2" y="15" rx=".5"></rect></svg></svg>`,
    content: `
      <section class="p-6 bg-white rounded shadow">
        <h2 class="text-2xl font-bold mb-2">Tiêu đề</h2>
        <p class="text-gray-700">Nội dung mô tả dài hơn...</p>
      </section>
    `
  });
  
  
    // 📋 FORM BLOCKS
    bm.add('form', {
      label: 'Form',
      category: '📋 Forms',
      media:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 5.5c0-.3-.5-.5-1.3-.5H3.4c-.8 0-1.3.2-1.3.5v3c0 .3.5.5 1.3.5h17.4c.8 0 1.3-.2 1.3-.5v-3zM21 8H3V6h18v2zM22 10.5c0-.3-.5-.5-1.3-.5H3.4c-.8 0-1.3.2-1.3.5v3c0 .3.5.5 1.3.5h17.4c.8 0 1.3-.2 1.3-.5v-3zM21 13H3v-2h18v2z"></path><rect width="10" height="3" x="2" y="15" rx=".5"></rect></svg>`,
      content: `
        <form class="space-y-4">
          <input type="text" placeholder="Họ tên" class="input-field" />
          <input type="email" placeholder="Email" class="input-field" />
          <input type="tel" placeholder="SĐT" class="input-field" />
          <button class="bg-primary text-white px-4 py-2 rounded w-full">Gửi thông tin</button>
        </form>
      `
    });
  
    bm.add('input', {
      label: 'Input',
      category: '📋 Forms',
      media:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 9c0-.6-.5-1-1.3-1H3.4C2.5 8 2 8.4 2 9v6c0 .6.5 1 1.3 1h17.4c.8 0 1.3-.4 1.3-1V9zm-1 6H3V9h18v6z"></path><path d="M4 10h1v4H4z"></path></svg>`,
      content: `<input type="text" class="input-field" placeholder="Nhập nội dung" />`
    });
  
    bm.add('textarea', {
      label: 'Textarea',
      category: '📋 Forms',
      media:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 7.5c0-.9-.5-1.5-1.3-1.5H3.4C2.5 6 2 6.6 2 7.5v9c0 .9.5 1.5 1.3 1.5h17.4c.8 0 1.3-.6 1.3-1.5v-9zM21 17H3V7h18v10z"></path><path d="M4 8h1v4H4zM19 7h1v10h-1zM20 8h1v1h-1zM20 15h1v1h-1z"></path></svg>`,
      content: `<textarea class="input-field" placeholder="Mô tả thêm..."></textarea>`
    });
  
    bm.add('select', {
      label: 'Select',
      category: '📋 Forms',
      media:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 9c0-.6-.5-1-1.3-1H3.4C2.5 8 2 8.4 2 9v6c0 .6.5 1 1.3 1h17.4c.8 0 1.3-.4 1.3-1V9zm-1 6H3V9h18v6z"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 7.5c0-.9-.5-1.5-1.3-1.5H3.4C2.5 6 2 6.6 2 7.5v9c0 .9.5 1.5 1.3 1.5h17.4c.8 0 1.3-.6 1.3-1.5v-9zM21 17H3V7h18v10z"></path><path d="M4 8h1v4H4zM19 7h1v10h-1zM20 8h1v1h-1zM20 15h1v1h-1z"></path></svg></path><path d="M18.5 13l1.5-2h-3zM4 11.5h11v1H4z"></path><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 7.5c0-.9-.5-1.5-1.3-1.5H3.4C2.5 6 2 6.6 2 7.5v9c0 .9.5 1.5 1.3 1.5h17.4c.8 0 1.3-.6 1.3-1.5v-9zM21 17H3V7h18v10z"></path><path d="M4 8h1v4H4zM19 7h1v10h-1zM20 8h1v1h-1zM20 15h1v1h-1z"></path></svg><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 7.5c0-.9-.5-1.5-1.3-1.5H3.4C2.5 6 2 6.6 2 7.5v9c0 .9.5 1.5 1.3 1.5h17.4c.8 0 1.3-.6 1.3-1.5v-9zM21 17H3V7h18v10z"></path><path d="M4 8h1v4H4zM19 7h1v10h-1zM20 8h1v1h-1zM20 15h1v1h-1z"></path></svg><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 7.5c0-.9-.5-1.5-1.3-1.5H3.4C2.5 6 2 6.6 2 7.5v9c0 .9.5 1.5 1.3 1.5h17.4c.8 0 1.3-.6 1.3-1.5v-9zM21 17H3V7h18v10z"></path><path d="M4 8h1v4H4zM19 7h1v10h-1zM20 8h1v1h-1zM20 15h1v1h-1z"></path></svg><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 7.5c0-.9-.5-1.5-1.3-1.5H3.4C2.5 6 2 6.6 2 7.5v9c0 .9.5 1.5 1.3 1.5h17.4c.8 0 1.3-.6 1.3-1.5v-9zM21 17H3V7h18v10z"></path><path d="M4 8h1v4H4zM19 7h1v10h-1zM20 8h1v1h-1zM20 15h1v1h-1z"></path></svg></svg>`,
      content: `
        <div class="w-full p-2">
      <label class="block text-sm font-medium text-gray-700 mb-1">Chọn một mục</label>
      <select class="w-full border border-gray-300 rounded px-3 py-2 text-sm">
        <option>Option A</option>
        <option>Option B</option>
      </select>
    </div>
      `
    });
  
    bm.add('button', {
      label: 'Button',
      media:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 9c0-.6-.5-1-1.3-1H3.4C2.5 8 2 8.4 2 9v6c0 .6.5 1 1.3 1h17.4c.8 0 1.3-.4 1.3-1V9zm-1 6H3V9h18v6z"></path><path d="M4 11.5h16v1H4z"></path></svg>`,
      category: '📋 Forms',
      content: `<button class="bg-blue-500 text-white px-4 py-2 rounded">Gửi</button>`
    });
  
    bm.add('label', {
      label: 'Label',
      category: '📋 Forms',
      media:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 11.9c0-.6-.5-.9-1.3-.9H3.4c-.8 0-1.3.3-1.3.9V17c0 .5.5.9 1.3.9h17.4c.8 0 1.3-.4 1.3-.9V12zM21 17H3v-5h18v5z"></path><rect width="14" height="5" x="2" y="5" rx=".5"></rect><path d="M4 13h1v3H4z"></path></svg>`,
      content: `<label class="block text-gray-700">Nhãn văn bản</label>`
    });
  
    bm.add('checkbox', {
      label: 'Checkbox',
      category: '📋 Forms',
      media:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M10 17l-5-5 1.41-1.42L10 14.17l7.59-7.59L19 8m0-5H5c-1.11 0-2 .89-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5a2 2 0 0 0-2-2z"></path></svg>`,
      content: `
        <label class="flex items-center space-x-2">
          <input type="checkbox" /> <span>Đồng ý điều khoản</span>
        </label>
      `
    });
  
    bm.add('radio', {
      label: 'Radio',
      category: '📋 Forms',
      media:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8m0-18C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2m0 5c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5z"></path></svg>`,
      content: `
        <label class="flex items-center space-x-2">
          <input type="radio" name="radio-group" /> <span>Lựa chọn</span>
        </label>
      `
    });
  
    // ⭐ EXTRA UI
    bm.add('countdown-timer', {
      label: 'Countdown',
      category: '⭐ Extra',
      media:`<svg viewBox="0 0 24 24">
        <path fill="currentColor" d="M12 20C16.4 20 20 16.4 20 12S16.4 4 12 4 4 7.6 4 12 7.6 20 12 20M12 2C17.5 2 22 6.5 22 12S17.5 22 12 22C6.5 22 2 17.5 2 12C2 6.5 6.5 2 12 2M17 11.5V13H11V7H12.5V11.5H17Z"></path>
      </svg>`,
      content: `
        <div class="flex justify-center space-x-4 text-center">
          <div>
            <div class="text-4xl font-bold">10</div>
            <div class="text-sm text-gray-500">Ngày</div>
          </div>
          <div>
            <div class="text-4xl font-bold">23</div>
            <div class="text-sm text-gray-500">Giờ</div>
          </div>
          <div>
            <div class="text-4xl font-bold">45</div>
            <div class="text-sm text-gray-500">Phút</div>
          </div>
        </div>
      `
    });
  
    bm.add('tabs-block', {
      label: 'Tabs',
      category: '⭐ Extra',
      media:`<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M22 9.3c0-.8-.5-1.3-1.3-1.3H3.4C2.5 8 2 8.5 2 9.3v7.4c0 .8.5 1.3 1.3 1.3h17.4c.8 0 1.3-.5 1.3-1.3V9.3zM21 17H3V9h18v8z" fill-rule="nonzero"></path><rect x="3" y="5" width="4" height="2" rx=".5"></rect><rect x="8" y="5" width="4" height="2" rx=".5"></rect><rect x="13" y="5" width="4" height="2" rx=".5"></rect>
      </svg>`,
      content: `
        <div>
          <div class="flex space-x-4 border-b mb-4">
            <button class="py-2 px-4 font-semibold border-b-2 border-primary">Tab 1</button>
            <button class="py-2 px-4 text-gray-500">Tab 2</button>
          </div>
          <div class="text-gray-700">Nội dung tab 1</div>
        </div>
      `
    });
  
    bm.add('custom-code', {
      label: 'Custom Code',
      category: '⭐ Extra',
      media:`<svg viewBox="0 0 24 24">
        <path d="M14.6 16.6l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4m-5.2 0L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4z"></path>
      </svg>`,
      content: `<div><script>alert('Your custom JS here')</script></div>`
    });
  
    bm.add('tooltip', {
      label: 'Tooltip',
      category: '⭐ Extra',
      media:`<svg viewBox="0 0 24 24">
          <path d="M4 2h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2h-4l-4 4-4-4H4c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2m0 2v12h4.83L12 19.17 15.17 16H20V4H4z"></path>
        </svg>`,
      content: `
        <div class="relative group inline-block">
          <span class="text-blue-500 underline cursor-pointer">Hover me</span>
          <div class="absolute hidden group-hover:block bg-black text-white text-sm rounded py-1 px-2 bottom-full mb-2">Tooltip nội dung</div>
        </div>
      `
    });
  
    bm.add('typed-text', {
      label: 'Typed',
      category: '⭐ Extra',
      media:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300"><path d="M212.3 44l2.3 49.6h-6A60 60 0 00204 75c-3.2-6-7.5-10.5-12.9-13.3a44.9 44.9 0 00-21.1-4.3h-29.8V219c0 13 1.4 21 4.2 24.3 4 4.4 10 6.6 18.2 6.6h7.4v5.7H80.2V250h7.5c9 0 15.3-2.7 19-8.2 2.4-3.3 3.5-10.9 3.5-22.7V57.3H84.8a71 71 0 00-21.1 2.2 29 29 0 00-13.9 11.3 46.1 46.1 0 00-6.9 22.8H37L39.5 44h172.8zM245 22h18v256h-18z"></path></svg>`,
      content: `<span class="text-2xl font-bold" id="typed-text">Đang gõ...</span>`
    });
  
    // 📎 STYLES (Tailwind utility)
    editor.CssComposer.addRules(`
      .input-field {
        @apply border border-gray-300 px-4 py-2 rounded w-full;
      }
    `);


    //Style Manager
    st.addSector('layout', {
        name: 'Layout',
        open: false,
        buildProps: ['display', 'position', 'top', 'right', 'left', 'bottom', 'width', 'height', 'margin', 'padding'],
        properties: [
          { property: 'display' },
          { property: 'position' },
          { property: 'top' },
          { property: 'right' },
          { property: 'bottom' },
          { property: 'left' },
          { property: 'width' },
          { property: 'height' },
          { property: 'margin' },
          { property: 'padding' },
        ]
      });
    
      st.addSector('typography', {
        name: 'Typography',
        open: false,
        buildProps: ['font-family', 'font-size', 'font-weight', 'letter-spacing', 'color', 'line-height', 'text-align'],
        properties: [
          { property: 'font-family' },
          { property: 'font-size' },
          { property: 'font-weight' },
          { property: 'letter-spacing' },
          { property: 'line-height' },
          { property: 'color' },
          { property: 'text-align' },
        ]
      });

      st.addSector('background', {
        name: 'Background',
        open: false,
        buildProps: ['background-color', 'background-image', 'background-size', 'background-repeat'],
        properties: [
          { property: 'background-color' },
          { property: 'background-image' },
          { property: 'background-size' },
          { property: 'background-repeat' },
        ]
      });

      st.addSector('borders', {
        name: 'Borders',
        open: false,
        buildProps: ['border', 'border-radius', 'box-shadow'],
        properties: [
          { property: 'border' },
          { property: 'border-radius' },
          { property: 'box-shadow' },
        ]
      });

      st.addSector('flex', {
        name: 'Flexbox',
        open: false,
        buildProps: ['display', 'flex-direction', 'justify-content', 'align-items', 'align-content', 'order', 'flex', 'flex-grow', 'flex-shrink', 'flex-basis'],
      });
      
      const mergeTags = [
        { label: 'Company Name', tag: '{{ company_name }}' },
        { label: 'Form URL', tag: '{{ form_url }}' },
        { label: 'Logo URL', tag: '{{ logo_url }}' },
      ];
      editor.BlockManager.add('merge-tag-blocks', {
        label: 'Merge Tags',
        category: 'Dynamic',
        content: `<span>{{ company_name }}</span>`,
      });
      editor.Commands.add('open-merge-tag-popup', {
        run(editor) {
          const modal = editor.Modal;
          const content = document.createElement('div');
      
          mergeTags.forEach(tag => {
            const btn = document.createElement('button');
            btn.innerText = tag.label;
            btn.style.margin = '4px';
            btn.onclick = () => {
              const selected = editor.getSelected();
              const insertText = tag.tag;
      
              if (selected && selected.is('text')) {
                selected.view?.setContent(selected.view.getContent() + insertText);
              } else {
                editor.RichTextEditor?.insertHTML?.(insertText); // fallback
              }
      
              modal.close();
            };
      
            content.appendChild(btn);
          });
      
          modal.setTitle('Insert Merge Tag');
          modal.setContent(content);
          modal.open();
        }
      });
      editor.Panels.addButton('options', [{
        id: 'merge-tags',
        className: 'fa fa-tag',
        command: 'open-merge-tag-popup',
        attributes: { title: 'Insert Merge Tag' }
      }]);
  }
  