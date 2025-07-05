<template>
  <v-container fluid class="pa-0">
    <!-- Header -->
    <v-app-bar color="white" elevation="1" height="80">
      <v-container class="d-flex align-center justify-space-between">
        <v-toolbar-title class="text-h5 font-weight-bold text-grey-darken-4">
          Talent Pool Management Solution
        </v-toolbar-title>
        <div class="d-flex align-center">
          <v-chip size="small" color="grey-lighten-3" class="mr-4">
            <span class="text-caption text-grey-darken-1">Product Document</span>
          </v-chip>
          <v-chip size="small" color="blue-lighten-4" text-color="blue-darken-2">
            <span class="text-caption font-weight-medium">Version 1.0</span>
          </v-chip>
        </div>
      </v-container>
    </v-app-bar>

    <!-- Main Content -->
    <v-main class="bg-gradient-to-br" style="background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);">
      <v-container class="py-8">
        <v-card class="rounded-xl" elevation="3">
          <v-card-text class="pa-8">
            <!-- Overview Section -->
            <div class="d-flex align-center mb-6">
              <v-avatar color="blue" size="56" class="mr-4">
                <v-icon color="white" size="24">mdi-plus</v-icon>
              </v-avatar>
              <v-card-title class="text-h4 font-weight-bold pa-0">
                Tổng quan giải pháp
              </v-card-title>
            </div>

            <v-card-text class="text-body-1 text-grey-darken-1 mb-6 pa-0">
              Giải pháp Talent Pool Management là một hệ thống độc lập được thiết kế để tối ưu hóa việc thu thập, quản lý và duy trì kết nối với các ứng viên tiềm năng. Hệ thống tích hợp công nghệ AI tiên tiến, đặc biệt là Generative AI, để tự động hóa các tác vụ và đóng vai trò như một Nhân sự số (AI Agent) hỗ trợ đội ngũ tuyển dụng.
            </v-card-text>

            <!-- Key Features Cards -->
            <v-row class="mb-8">
              <v-col cols="12" md="4">
                <v-card color="blue-lighten-6" class="pa-6 h-100">
                  <div class="d-flex align-center mb-3">
                    <v-icon color="blue" class="mr-2">mdi-check-circle</v-icon>
                    <v-card-subtitle class="font-weight-bold text-grey-darken-4 pa-0">
                      Hệ thống độc lập
                    </v-card-subtitle>
                  </div>
                  <v-card-text class="text-caption text-grey-darken-1 pa-0">
                    Vận hành như một hệ thống độc lập với đầy đủ chức năng quản lý talent pool, không phụ thuộc vào các hệ thống tuyển dụng khác.
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="4">
                <v-card color="blue-lighten-6" class="pa-6 h-100">
                  <div class="d-flex align-center mb-3">
                    <v-icon color="blue" class="mr-2">mdi-lightning-bolt</v-icon>
                    <v-card-subtitle class="font-weight-bold text-grey-darken-4 pa-0">
                      Ứng dụng AI
                    </v-card-subtitle>
                  </div>
                  <v-card-text class="text-caption text-grey-darken-1 pa-0">
                    Tích hợp công nghệ AI, đặc biệt là GenAI, để tự động hóa các tác vụ phân tích, phân loại và tương tác với ứng viên.
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="4">
                <v-card color="blue-lighten-6" class="pa-6 h-100">
                  <div class="d-flex align-center mb-3">
                    <v-icon color="blue" class="mr-2">mdi-chat</v-icon>
                    <v-card-subtitle class="font-weight-bold text-grey-darken-4 pa-0">
                      Nhân sự số
                    </v-card-subtitle>
                  </div>
                  <v-card-text class="text-caption text-grey-darken-1 pa-0">
                    Hoạt động như một AI Agent thông minh, nhận nhiệm vụ và tương tác với người dùng để thực hiện các tác vụ quản lý talent pool.
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Main Features Section -->
            <div class="mb-10">
              <div class="d-flex align-center mb-6">
                <v-avatar color="indigo" size="56" class="mr-4">
                  <v-icon color="white" size="24">mdi-briefcase</v-icon>
                </v-avatar>
                <v-card-title class="text-h4 font-weight-bold pa-0">
                  Chức năng chính
                </v-card-title>
              </div>

              <v-row class="mb-8">
                <!-- Feature 1 -->
                <v-col cols="12" md="6">
                  <v-card variant="default" class="pa-6 h-100">
                    <v-card-title class="text-h6 font-weight-bold mb-3 pa-0">
                      Thu thập và quản lý talent
                    </v-card-title>
                    <v-list class="pa-0">
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Tự động thu thập thông tin ứng viên từ nhiều nguồn</span>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Phân tích và phân loại ứng viên theo kỹ năng, kinh nghiệm</span>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Tạo và quản lý hồ sơ ứng viên với thông tin chi tiết</span>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Tìm kiếm và lọc ứng viên theo nhiều tiêu chí</span>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-card>
                </v-col>

                <!-- Feature 2 -->
                <v-col cols="12" md="6">
                  <v-card variant="default" class="pa-6 h-100">
                    <v-card-title class="text-h6 font-weight-bold mb-3 pa-0">
                      Chiến dịch thu hút ứng viên
                    </v-card-title>
                    <v-list class="pa-0">
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Tạo và quản lý chiến dịch thu hút ứng viên</span>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Tự động tạo nội dung truyền thông phù hợp với từng đối tượng</span>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Phân tích hiệu quả chiến dịch và đề xuất cải tiến</span>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Tự động điều chỉnh chiến lược dựa trên phản hồi</span>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-card>
                </v-col>

                <!-- Feature 3 -->
                <v-col cols="12" md="6">
                  <v-card variant="default" class="pa-6 h-100">
                    <v-card-title class="text-h6 font-weight-bold mb-3 pa-0">
                      Duy trì kết nối ứng viên
                    </v-card-title>
                    <v-list class="pa-0">
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Tự động gửi thông tin, cập nhật định kỳ</span>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Phân tích mức độ tương tác và điều chỉnh chiến lược</span>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Tổ chức sự kiện và hoạt động tương tác</span>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Cá nhân hóa nội dung theo sở thích và mối quan tâm</span>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-card>
                </v-col>

                <!-- Feature 4 -->
                <v-col cols="12" md="6">
                  <v-card variant="default" class="pa-6 h-100">
                    <v-card-title class="text-h6 font-weight-bold mb-3 pa-0">
                      AI Agent (Nhân sự số)
                    </v-card-title>
                    <v-list class="pa-0">
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Tự động nhận và thực hiện nhiệm vụ</span>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Tương tác với người dùng qua giao diện timeline</span>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Đề xuất hành động và yêu cầu phê duyệt khi cần</span>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item class="pa-0 mb-2">
                        <template v-slot:prepend>
                          <v-icon color="green" size="20" class="mr-2">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-content class="pa-0">
                          <span class="text-body-2 text-grey-darken-1">Học hỏi từ phản hồi để cải thiện hiệu suất</span>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-card>
                </v-col>
              </v-row>
            </div>

            <!-- AI Agent Timeline Interface -->
            <div class="mb-10">
              <div class="d-flex align-center mb-6">
                <v-avatar color="purple" size="56" class="mr-4">
                  <v-icon color="white" size="24">mdi-clipboard-text</v-icon>
                </v-avatar>
                <v-card-title class="text-h4 font-weight-bold pa-0">
                  Giao diện tương tác AI Agent
                </v-card-title>
              </div>

              <v-card variant="default" class="pa-6 mb-6">
                <v-card-title class="text-h6 font-weight-bold mb-4 pa-0">
                  Thiết kế Timeline
                </v-card-title>
                <v-card-text class="text-body-1 text-grey-darken-1 mb-4 pa-0">
                  Giao diện tương tác giữa AI Agent và người dùng được thiết kế theo dạng timeline, hiển thị các sự kiện, hoạt động và tương tác theo thời gian thực. Mỗi sự kiện trong timeline có thể chứa dữ liệu có cấu trúc và các thành phần tương tác.
                </v-card-text>
                
                <!-- Timeline Demo -->
                <v-card color="grey-lighten-4" class="pa-6 mb-6">
                  <v-card-subtitle class="font-weight-medium text-grey-darken-4 mb-4 pa-0">
                    Minh họa Timeline
                  </v-card-subtitle>
                  
                  <div class="timeline-container">
                    <!-- Timeline Item 1 -->
                    <div class="timeline-item mb-8">
                      <v-card class="timeline-card pa-4" elevation="1">
                        <div class="d-flex justify-space-between align-center mb-2">
                          <v-chip size="small" color="blue" variant="flat">
                            <span class="text-caption font-weight-medium">AI Agent</span>
                          </v-chip>
                          <span class="text-caption text-grey">10:15 AM</span>
                        </div>
                        <v-card-text class="text-body-2 text-grey-darken-1 mb-3 pa-0">
                          Đã tạo chiến dịch thu hút ứng viên cho vị trí "Senior Developer" dựa trên yêu cầu của bạn.
                        </v-card-text>
                        <v-card color="blue-lighten-5" class="pa-3 mb-3">
                          <v-card-subtitle class="text-caption font-weight-medium text-grey-darken-4 mb-2 pa-0">
                            Chi tiết chiến dịch:
                          </v-card-subtitle>
                          <v-list class="pa-0">
                            <v-list-item class="pa-0 text-caption text-grey-darken-1">
                              - Đối tượng: Developers với 5+ năm kinh nghiệm
                            </v-list-item>
                            <v-list-item class="pa-0 text-caption text-grey-darken-1">
                              - Kênh: LinkedIn, Tech forums
                            </v-list-item>
                            <v-list-item class="pa-0 text-caption text-grey-darken-1">
                              - Thời gian: 15/06 - 30/06/2023
                            </v-list-item>
                          </v-list>
                        </v-card>
                        <div class="d-flex ga-2">
                          <v-btn size="small" color="blue" variant="flat">Phê duyệt</v-btn>
                          <v-btn size="small" variant="outlined">Chỉnh sửa</v-btn>
                          <v-btn size="small" variant="outlined">Xem chi tiết</v-btn>
                        </div>
                      </v-card>
                    </div>
                    
                    <!-- Timeline Item 2 -->
                    <div class="timeline-item mb-8">
                      <v-card class="timeline-card pa-4" elevation="1">
                        <div class="d-flex justify-space-between align-center mb-2">
                          <v-chip size="small" color="green" variant="flat">
                            <span class="text-caption font-weight-medium">Người dùng</span>
                          </v-chip>
                          <span class="text-caption text-grey">10:20 AM</span>
                        </div>
                        <v-card-text class="text-body-2 text-grey-darken-1 mb-3 pa-0">
                          Đã phê duyệt chiến dịch với một số điều chỉnh về thời gian.
                        </v-card-text>
                        <v-card color="green-lighten-5" class="pa-3 mb-3">
                          <v-card-subtitle class="text-caption font-weight-medium text-grey-darken-4 mb-2 pa-0">
                            Điều chỉnh:
                          </v-card-subtitle>
                          <v-card-text class="text-caption text-grey-darken-1 pa-0">
                            Thời gian chiến dịch: 20/06 - 10/07/2023
                          </v-card-text>
                        </v-card>
                      </v-card>
                    </div>
                    
                    <!-- Timeline Item 3 -->
                    <div class="timeline-item">
                      <v-card class="timeline-card pa-4" elevation="1">
                        <div class="d-flex justify-space-between align-center mb-2">
                          <v-chip size="small" color="blue" variant="flat">
                            <span class="text-caption font-weight-medium">AI Agent</span>
                          </v-chip>
                          <span class="text-caption text-grey">11:45 AM</span>
                        </div>
                        <v-card-text class="text-body-2 text-grey-darken-1 mb-3 pa-0">
                          Đã phát hiện 5 ứng viên tiềm năng phù hợp cao với vị trí. Đề xuất kết nối ngay.
                        </v-card-text>
                        <v-card color="blue-lighten-5" class="pa-3 mb-3">
                          <v-card-subtitle class="text-caption font-weight-medium text-grey-darken-4 mb-2 pa-0">
                            Ứng viên tiềm năng:
                          </v-card-subtitle>
                          <div class="d-flex flex-column ga-2">
                            <div class="d-flex align-center justify-space-between">
                              <div class="d-flex align-center">
                                <v-avatar size="24" color="grey-lighten-1" class="mr-2">
                                  <span class="text-caption">NT</span>
                                </v-avatar>
                                <span class="text-caption font-weight-medium">Nguyễn Thành</span>
                              </div>
                              <v-chip size="x-small" color="green-lighten-4" text-color="green-darken-2">
                                95% phù hợp
                              </v-chip>
                            </div>
                            <div class="d-flex align-center justify-space-between">
                              <div class="d-flex align-center">
                                <v-avatar size="24" color="grey-lighten-1" class="mr-2">
                                  <span class="text-caption">LH</span>
                                </v-avatar>
                                <span class="text-caption font-weight-medium">Lê Hương</span>
                              </div>
                              <v-chip size="x-small" color="green-lighten-4" text-color="green-darken-2">
                                92% phù hợp
                              </v-chip>
                            </div>
                          </div>
                        </v-card>
                        <div class="d-flex ga-2">
                          <v-btn size="small" color="blue" variant="flat">Phê duyệt kết nối</v-btn>
                          <v-btn size="small" variant="outlined">Xem chi tiết</v-btn>
                        </div>
                      </v-card>
                    </div>
                  </div>
                </v-card>
                
                <div class="text-grey-darken-1">
                  <v-card-subtitle class="font-weight-medium text-grey-darken-4 mb-2 pa-0">
                    Đặc điểm của giao diện timeline:
                  </v-card-subtitle>
                  <v-list class="pa-0">
                    <v-list-item class="pa-0 text-body-2">
                      <template v-slot:prepend>
                        <span class="mr-2">•</span>
                      </template>
                      Hiển thị các sự kiện theo thứ tự thời gian
                    </v-list-item>
                    <v-list-item class="pa-0 text-body-2">
                      <template v-slot:prepend>
                        <span class="mr-2">•</span>
                      </template>
                      Phân biệt rõ ràng giữa hành động của AI Agent và người dùng
                    </v-list-item>
                    <v-list-item class="pa-0 text-body-2">
                      <template v-slot:prepend>
                        <span class="mr-2">•</span>
                      </template>
                      Tích hợp các thành phần tương tác như nút phê duyệt, chỉnh sửa
                    </v-list-item>
                    <v-list-item class="pa-0 text-body-2">
                      <template v-slot:prepend>
                        <span class="mr-2">•</span>
                      </template>
                      Hiển thị dữ liệu có cấu trúc trong các khung thông tin
                    </v-list-item>
                    <v-list-item class="pa-0 text-body-2">
                      <template v-slot:prepend>
                        <span class="mr-2">•</span>
                      </template>
                      Cung cấp trạng thái và tiến độ của các hoạt động
                    </v-list-item>
                  </v-list>
                </div>
              </v-card>
            </div>

            <!-- Use Cases Section -->
            <div class="mb-10">
              <div class="d-flex align-center mb-6">
                <v-avatar color="green" size="56" class="mr-4">
                  <v-icon color="white" size="24">mdi-arrow-right</v-icon>
                </v-avatar>
                <v-card-title class="text-h4 font-weight-bold pa-0">
                  Kịch bản sử dụng
                </v-card-title>
              </div>

              <div class="d-flex flex-column ga-6">
                <!-- Use Case 1 -->
                <v-card variant="default" class="pa-6">
                  <v-card-title class="text-h6 font-weight-bold mb-4 pa-0">
                    Kịch bản 1: Tạo chiến dịch thu hút ứng viên
                  </v-card-title>
                  <div class="d-flex flex-column ga-4">
                    <!-- Bước 1 -->
                    <v-card color="grey-lighten-4" class="pa-4">
                      <v-card-subtitle class="font-weight-medium text-grey-darken-4 mb-2 pa-0">
                        Bước 1: Khởi tạo chiến dịch
                      </v-card-subtitle>
                      <div class="d-flex align-start ga-3">
                        <v-avatar color="green-lighten-2" size="32">
                          <span class="text-caption font-weight-bold text-green-darken-2">ND</span>
                        </v-avatar>
                        <div class="flex-grow-1">
                          <v-card-text class="text-body-2 text-grey-darken-1 mb-1 pa-0">
                            <span class="font-weight-medium">Người dùng:</span> "Tôi cần tạo một chiến dịch thu hút ứng viên cho vị trí Data Scientist."
                          </v-card-text>
                          <v-card color="blue-lighten-5" class="pa-3 mt-3 mb-3" style="border-left: 4px solid #1976d2;">
                            <v-card-text class="text-body-2 text-grey-darken-1 pa-0">
                              <span class="font-weight-medium">AI Agent:</span> "Tôi sẽ giúp bạn tạo chiến dịch thu hút ứng viên cho vị trí Data Scientist. Để tạo chiến dịch hiệu quả, tôi cần một số thông tin:"
                            </v-card-text>
                            <v-list class="pa-0 mt-2">
                              <v-list-item class="pa-0 text-body-2">1. Yêu cầu kỹ năng và kinh nghiệm cụ thể cho vị trí này?</v-list-item>
                              <v-list-item class="pa-0 text-body-2">2. Thời gian dự kiến cho chiến dịch?</v-list-item>
                              <v-list-item class="pa-0 text-body-2">3. Kênh tiếp cận ưu tiên (LinkedIn, diễn đàn chuyên ngành, email...)?</v-list-item>
                            </v-list>
                          </v-card>
                          <v-card-text class="text-body-2 text-grey-darken-1 mb-1 pa-0">
                            <span class="font-weight-medium">Người dùng:</span> "Chúng tôi cần người có ít nhất 3 năm kinh nghiệm với Python, kiến thức về machine learning và xử lý dữ liệu lớn. Thời gian chiến dịch là 3 tuần, từ 1/7 đến 21/7. Ưu tiên tiếp cận qua LinkedIn và các diễn đàn AI/ML."
                          </v-card-text>
                        </div>
                      </div>
                    </v-card>

                    <!-- Bước 2 -->
                    <v-card color="grey-lighten-4" class="pa-4">
                      <v-card-subtitle class="font-weight-medium text-grey-darken-4 mb-2 pa-0">
                        Bước 2: AI Agent phân tích và đề xuất
                      </v-card-subtitle>
                      <div class="d-flex align-start ga-3">
                        <v-avatar color="blue-lighten-2" size="32">
                          <span class="text-caption font-weight-bold text-blue-darken-2">AI</span>
                        </v-avatar>
                        <div class="flex-grow-1">
                          <v-card-text class="text-body-2 text-grey-darken-1 mb-3 pa-0">
                            "Dựa trên thông tin bạn cung cấp, tôi đã phân tích dữ liệu từ talent pool hiện có và thị trường lao động. Tôi đề xuất chiến dịch như sau:"
                          </v-card-text>
                          <v-card variant="default" class="pa-4 mb-3">
                            <v-card-subtitle class="text-body-2 font-weight-medium text-grey-darken-4 mb-2 pa-0">
                              Chiến dịch thu hút Data Scientist
                            </v-card-subtitle>
                            <v-list class="pa-0">
                              <v-list-item class="pa-0 text-body-2 text-grey-darken-1">
                                <span class="font-weight-medium">Đối tượng:</span> Data Scientists với 3+ năm kinh nghiệm Python, ML/AI
                              </v-list-item>
                              <v-list-item class="pa-0 text-body-2 text-grey-darken-1">
                                <span class="font-weight-medium">Thời gian:</span> 01/07 - 21/07/2023
                              </v-list-item>
                              <v-list-item class="pa-0 text-body-2 text-grey-darken-1">
                                <span class="font-weight-medium">Kênh tiếp cận:</span> LinkedIn (60%), Kaggle & ML Forums (30%), Email (10%)
                              </v-list-item>
                              <v-list-item class="pa-0 text-body-2 text-grey-darken-1">
                                <span class="font-weight-medium">Nội dung:</span> Nhấn mạnh vào dự án phân tích dữ liệu lớn, cơ hội nghiên cứu và phát triển mô hình ML tiên tiến
                              </v-list-item>
                              <v-list-item class="pa-0 text-body-2 text-grey-darken-1">
                                <span class="font-weight-medium">Ước tính:</span> Tiếp cận 200+ ứng viên tiềm năng, dự kiến 30-40 ứng viên quan tâm
                              </v-list-item>
                            </v-list>
                          </v-card>
                          <v-card-text class="text-body-2 text-grey-darken-1 pa-0">
                            "Tôi cũng đã tạo sẵn các mẫu nội dung cho các kênh khác nhau. Bạn có muốn xem trước và phê duyệt chiến dịch này không?"
                          </v-card-text>
                        </div>
                      </div>
                    </v-card>

                    <!-- Bước 3 -->
                    <v-card color="grey-lighten-4" class="pa-4">
                      <v-card-subtitle class="font-weight-medium text-grey-darken-4 mb-2 pa-0">
                        Bước 3: Phê duyệt và điều chỉnh
                      </v-card-subtitle>
                      <div class="d-flex align-start ga-3">
                        <v-avatar color="green-lighten-2" size="32">
                          <span class="text-caption font-weight-bold text-green-darken-2">ND</span>
                        </v-avatar>
                        <div class="flex-grow-1">
                          <v-card-text class="text-body-2 text-grey-darken-1 mb-1 pa-0">
                            <span class="font-weight-medium">Người dùng:</span> "Đề xuất tốt, nhưng tôi muốn thêm kỹ năng về AWS và cloud computing vào yêu cầu. Cũng nên nhấn mạnh về môi trường làm việc linh hoạt của chúng tôi."
                          </v-card-text>
                          <v-card color="blue-lighten-5" class="pa-3 mt-3 mb-3" style="border-left: 4px solid #1976d2;">
                            <v-card-text class="text-body-2 text-grey-darken-1 pa-0">
                              <span class="font-weight-medium">AI Agent:</span> "Tôi đã cập nhật chiến dịch với yêu cầu về AWS và cloud computing, đồng thời điều chỉnh nội dung để nhấn mạnh về môi trường làm việc linh hoạt. Dưới đây là phiên bản cập nhật:"
                            </v-card-text>
                            <v-card variant="default" class="pa-3 mt-2">
                              <v-card-subtitle class="text-caption font-weight-medium text-grey-darken-4 mb-2 pa-0">
                                Chiến dịch làm ấm talent pool - Nhóm kỹ thuật
                              </v-card-subtitle>
                              <v-list class="pa-0">
                                <v-list-item class="pa-0 text-caption text-grey-darken-1 mb-2">
                                  <span class="font-weight-medium">1. Webinar chuyên đề:</span> Tổ chức webinar về "Xu hướng công nghệ mới trong phát triển phần mềm" với diễn giả là chuyên gia kỹ thuật của công ty
                                </v-list-item>
                                <v-list-item class="pa-0 text-caption text-grey-darken-1 mb-2">
                                  <span class="font-weight-medium">2. Bản tin kỹ thuật:</span> Gửi bản tin hàng tháng với nội dung về công nghệ mới, dự án thú vị và văn hóa đội ngũ kỹ thuật
                                </v-list-item>
                                <v-list-item class="pa-0 text-caption text-grey-darken-1 mb-2">
                                  <span class="font-weight-medium">3. Thử thách kỹ thuật:</span> Tổ chức mini hackathon với giải thưởng và cơ hội kết nối
                                </v-list-item>
                                <v-list-item class="pa-0 text-caption text-grey-darken-1 mb-2">
                                  <span class="font-weight-medium">4. Cá nhân hóa nội dung:</span> Gửi thông tin về các vị trí mới phù hợp với kỹ năng và sở thích của từng ứng viên
                                </v-list-item>
                              </v-list>
                              <v-divider class="my-2"></v-divider>
                              <div class="text-caption">
                                <span class="font-weight-medium text-grey-darken-4">Thời gian thực hiện:</span>
                                <span class="text-grey-darken-1"> 4 tuần (15/07 - 15/08/2023)</span>
                              </div>
                            </v-card>
                          </v-card>
                        </div>
                      </div>
                    </v-card>

                    <!-- Bước 4 -->
                    <v-card color="grey-lighten-4" class="pa-4">
                      <v-card-subtitle class="font-weight-medium text-grey-darken-4 mb-2 pa-0">
                        Bước 4: Triển khai và theo dõi
                      </v-card-subtitle>
                      <div class="d-flex align-start ga-3">
                        <v-avatar color="blue-lighten-2" size="32">
                          <span class="text-caption font-weight-bold text-blue-darken-2">AI</span>
                        </v-avatar>
                        <div class="flex-grow-1">
                          <v-card-text class="text-body-2 text-grey-darken-1 mb-3 pa-0">
                            "Tôi đã bắt đầu triển khai chiến dịch thu hút ứng viên Data Scientist. Hệ thống sẽ tự động theo dõi và báo cáo kết quả theo thời gian thực."
                          </v-card-text>
                          <v-card variant="default" class="pa-4 mb-3">
                            <v-card-subtitle class="text-body-2 font-weight-medium text-grey-darken-4 mb-2 pa-0">
                              Trạng thái chiến dịch
                            </v-card-subtitle>
                            <div class="d-flex flex-column ga-3">
                              <v-row>
                                <v-col cols="6">
                                  <div class="text-caption text-grey mb-1">Tỷ lệ mở email</div>
                                  <div class="d-flex align-end">
                                    <span class="text-h6 font-weight-bold text-grey-darken-4">58%</span>
                                    <v-chip size="x-small" color="green-lighten-4" text-color="green-darken-2" class="ml-2">
                                      ↑ 16%
                                    </v-chip>
                                  </div>
                                </v-col>
                                <v-col cols="6">
                                  <div class="text-caption text-grey mb-1">Đăng ký webinar</div>
                                  <div class="d-flex align-end">
                                    <span class="text-h6 font-weight-bold text-grey-darken-4">42</span>
                                    <v-chip size="x-small" color="green-lighten-4" text-color="green-darken-2" class="ml-2">
                                      ↑ 28%
                                    </v-chip>
                                  </div>
                                </v-col>
                              </v-row>
                              <div>
                                <div class="text-caption text-grey mb-1">Phản hồi tích cực</div>
                                <div class="d-flex align-center justify-space-between">
                                  <span class="text-body-2 font-weight-medium text-grey-darken-4">15 ứng viên đã phản hồi tích cực</span>
                                  <v-chip size="small" color="green-lighten-4" text-color="green-darken-2">Vượt mục tiêu</v-chip>
                                </div>
                              </div>
                            </div>
                          </v-card>
                          <v-card-text class="text-body-2 text-grey-darken-1 pa-0">
                            "Dựa trên phản hồi, tôi đề xuất tăng cường nội dung về công nghệ cloud và DevOps vì đây là chủ đề được quan tâm nhiều nhất. Tôi cũng đề xuất mở rộng chiến dịch thêm 2 tuần để tối ưu kết quả. Bạn có đồng ý không?"
                          </v-card-text>
                        </div>
                      </div>
                    </v-card>
                  </div>
                </v-card>

                <!-- Use Case 2 -->
                <v-card variant="default" class="pa-6">
                  <v-card-title class="text-h6 font-weight-bold mb-4 pa-0">
                    Kịch bản 2: Duy trì kết nối với talent pool
                  </v-card-title>
                  <div class="d-flex flex-column ga-4">
                    <!-- Bước 1 -->
                    <v-card color="grey-lighten-4" class="pa-4">
                      <v-card-subtitle class="font-weight-medium text-grey-darken-4 mb-2 pa-0">
                        Bước 1: Phân tích mức độ tương tác
                      </v-card-subtitle>
                      <div class="d-flex align-start ga-3">
                        <v-avatar color="blue-lighten-2" size="32">
                          <span class="text-caption font-weight-bold text-blue-darken-2">AI</span>
                        </v-avatar>
                        <div class="flex-grow-1">
                          <v-card-text class="text-body-2 text-grey-darken-1 mb-3 pa-0">
                            "Tôi đã phân tích mức độ tương tác của talent pool trong 3 tháng qua và nhận thấy có sự sụt giảm 15% trong tương tác với nhóm ứng viên kỹ thuật. Dưới đây là báo cáo chi tiết:"
                          </v-card-text>
                          <v-card variant="default" class="pa-4 mb-3">
                            <v-card-subtitle class="text-body-2 font-weight-medium text-grey-darken-4 mb-2 pa-0">
                              Phân tích tương tác talent pool
                            </v-card-subtitle>
                            <div class="d-flex flex-column ga-3">
                              <v-row>
                                <v-col cols="6">
                                  <div class="text-caption text-grey mb-1">Tỷ lệ mở email</div>
                                  <div class="d-flex align-end">
                                    <span class="text-h6 font-weight-bold text-grey-darken-4">42%</span>
                                    <v-chip size="x-small" color="red-lighten-4" text-color="red-darken-2" class="ml-2">
                                      ↓ 8%
                                    </v-chip>
                                  </div>
                                </v-col>
                                <v-col cols="6">
                                  <div class="text-caption text-grey mb-1">Tỷ lệ click</div>
                                  <div class="d-flex align-end">
                                    <span class="text-h6 font-weight-bold text-grey-darken-4">12%</span>
                                    <v-chip size="x-small" color="red-lighten-4" text-color="red-darken-2" class="ml-2">
                                      ↓ 5%
                                    </v-chip>
                                  </div>
                                </v-col>
                              </v-row>
                              <div>
                                <div class="text-caption text-grey mb-1">Nhóm có mức độ tương tác thấp nhất</div>
                                <div class="d-flex align-center justify-space-between">
                                  <span class="text-body-2 font-weight-medium text-grey-darken-4">Kỹ sư phần mềm (3-5 năm KN)</span>
                                  <v-chip size="small" color="amber-lighten-4" text-color="amber-darken-2">Cần chú ý</v-chip>
                                </div>
                              </div>
                            </div>
                          </v-card>
                          <v-card-text class="text-body-2 text-grey-darken-1 pa-0">
                            "Tôi đề xuất tạo một chiến dịch làm ấm lại mối quan hệ với nhóm ứng viên kỹ thuật. Bạn có muốn tôi đề xuất kế hoạch cụ thể không?"
                          </v-card-text>
                        </div>
                      </div>
                    </v-card>

                    <!-- Bước 2 -->
                    <v-card color="grey-lighten-4" class="pa-4">
                      <v-card-subtitle class="font-weight-medium text-grey-darken-4 mb-2 pa-0">
                        Bước 2: Đề xuất chiến lược duy trì kết nối
                      </v-card-subtitle>
                      <div class="d-flex align-start ga-3">
                        <v-avatar color="green-lighten-2" size="32">
                          <span class="text-caption font-weight-bold text-green-darken-2">ND</span>
                        </v-avatar>
                        <div class="flex-grow-1">
                          <v-card-text class="text-body-2 text-grey-darken-1 mb-1 pa-0">
                            <span class="font-weight-medium">Người dùng:</span> "Vâng, hãy đề xuất kế hoạch làm ấm lại mối quan hệ với nhóm kỹ thuật."
                          </v-card-text>
                          <v-card color="blue-lighten-5" class="pa-3 mt-3" style="border-left: 4px solid #1976d2;">
                            <v-card-text class="text-body-2 text-grey-darken-1 pa-0">
                              <span class="font-weight-medium">AI Agent:</span> "Dựa trên phân tích dữ liệu và xu hướng trong ngành, tôi đề xuất kế hoạch làm ấm mối quan hệ như sau:"
                            </v-card-text>
                            <v-card variant="default" class="pa-3 mt-2">
                              <v-card-subtitle class="text-caption font-weight-medium text-grey-darken-4 mb-2 pa-0">
                                Chiến dịch làm ấm talent pool - Nhóm kỹ thuật
                              </v-card-subtitle>
                              <v-list class="pa-0">
                                <v-list-item class="pa-0 text-caption text-grey-darken-1 mb-2">
                                  <span class="font-weight-medium">1. Webinar chuyên đề:</span> Tổ chức webinar về "Xu hướng công nghệ mới trong phát triển phần mềm" với diễn giả là chuyên gia kỹ thuật của công ty
                                </v-list-item>
                                <v-list-item class="pa-0 text-caption text-grey-darken-1 mb-2">
                                  <span class="font-weight-medium">2. Bản tin kỹ thuật:</span> Gửi bản tin hàng tháng với nội dung về công nghệ mới, dự án thú vị và văn hóa đội ngũ kỹ thuật
                                </v-list-item>
                                <v-list-item class="pa-0 text-caption text-grey-darken-1 mb-2">
                                  <span class="font-weight-medium">3. Thử thách kỹ thuật:</span> Tổ chức mini hackathon với giải thưởng và cơ hội kết nối
                                </v-list-item>
                                <v-list-item class="pa-0 text-caption text-grey-darken-1 mb-2">
                                  <span class="font-weight-medium">4. Cá nhân hóa nội dung:</span> Gửi thông tin về các vị trí mới phù hợp với kỹ năng và sở thích của từng ứng viên
                                </v-list-item>
                              </v-list>
                              <v-divider class="my-2"></v-divider>
                              <div class="text-caption">
                                <span class="font-weight-medium text-grey-darken-4">Thời gian thực hiện:</span>
                                <span class="text-grey-darken-1"> 4 tuần (15/07 - 15/08/2023)</span>
                              </div>
                            </v-card>
                          </v-card>
                        </div>
                      </div>
                    </v-card>

                    <!-- Bước 3 -->
                    <v-card color="grey-lighten-4" class="pa-4">
                      <v-card-subtitle class="font-weight-medium text-grey-darken-4 mb-2 pa-0">
                        Bước 3: Triển khai và cá nhân hóa nội dung
                      </v-card-subtitle>
                      <div class="d-flex align-start ga-3">
                        <v-avatar color="green-lighten-2" size="32">
                          <span class="text-caption font-weight-bold text-green-darken-2">ND</span>
                        </v-avatar>
                        <div class="flex-grow-1">
                          <v-card-text class="text-body-2 text-grey-darken-1 mb-1 pa-0">
                            <span class="font-weight-medium">Người dùng:</span> "Kế hoạch tốt. Hãy triển khai webinar và bản tin trước. Tôi muốn xem trước nội dung trước khi gửi."
                          </v-card-text>
                          <v-card color="blue-lighten-5" class="pa-3 mt-3" style="border-left: 4px solid #1976d2;">
                            <v-card-text class="text-body-2 text-grey-darken-1 pa-0">
                              <span class="font-weight-medium">AI Agent:</span> "Tôi sẽ ưu tiên triển khai webinar và bản tin kỹ thuật. Dưới đây là nội dung đề xuất cho bản tin đầu tiên:"
                            </v-card-text>
                            <v-card variant="default" class="pa-3 mt-2">
                              <v-card-subtitle class="text-caption font-weight-medium text-grey-darken-4 mb-2 pa-0">
                                Bản tin Tech Insights - Tháng 7/2023
                              </v-card-subtitle>
                              <div class="text-caption text-grey-darken-1 d-flex flex-column ga-2">
                                <div><span class="font-weight-medium">Tiêu đề:</span> "Khám phá tương lai công nghệ cùng [Tên Công ty]"</div>
                                <div><span class="font-weight-medium">Nội dung chính:</span></div>
                                <v-list class="pa-0">
                                  <v-list-item class="pa-0 text-caption">• Xu hướng microservices và cloud-native applications</v-list-item>
                                  <v-list-item class="pa-0 text-caption">• Phỏng vấn với Lead Developer về dự án mới</v-list-item>
                                  <v-list-item class="pa-0 text-caption">• Thông báo về webinar sắp tới với chuyên gia trong ngành</v-list-item>
                                  <v-list-item class="pa-0 text-caption">• Spotlight: Văn hóa làm việc tại đội ngũ kỹ thuật</v-list-item>
                                </v-list>
                                <div>Mỗi phần sẽ được cá nhân hóa dựa trên sở thích và lĩnh vực chuyên môn của từng ứng viên.</div>
                              </div>
                            </v-card>
                            <v-card-text class="text-body-2 text-grey-darken-1 mt-2 pa-0">Tôi cũng đã lên kế hoạch cho webinar với các diễn giả tiềm năng và chủ đề chi tiết. Bạn muốn xem chi tiết không?</v-card-text>
                          </v-card>
                        </div>
                      </div>
                    </v-card>

                    <!-- Bước 4 -->
                    <v-card color="grey-lighten-4" class="pa-4">
                      <v-card-subtitle class="font-weight-medium text-grey-darken-4 mb-2 pa-0">
                        Bước 4: Theo dõi và điều chỉnh
                      </v-card-subtitle>
                      <div class="d-flex align-start ga-3">
                        <v-avatar color="blue-lighten-2" size="32">
                          <span class="text-caption font-weight-bold text-blue-darken-2">AI</span>
                        </v-avatar>
                        <div class="flex-grow-1">
                          <v-card-text class="text-body-2 text-grey-darken-1 mb-3 pa-0">
                            "Sau 2 tuần triển khai chiến dịch làm ấm mối quan hệ, tôi đã ghi nhận những kết quả tích cực:"
                          </v-card-text>
                          <v-card variant="default" class="pa-4 mb-3">
                            <v-card-subtitle class="text-body-2 font-weight-medium text-grey-darken-4 mb-2 pa-0">
                              Kết quả chiến dịch
                            </v-card-subtitle>
                            <div class="d-flex flex-column ga-3">
                              <v-row>
                                <v-col cols="6">
                                  <div class="text-caption text-grey mb-1">Tỷ lệ mở email</div>
                                  <div class="d-flex align-end">
                                    <span class="text-h6 font-weight-bold text-grey-darken-4">58%</span>
                                    <v-chip size="x-small" color="green-lighten-4" text-color="green-darken-2" class="ml-2">
                                      ↑ 16%
                                    </v-chip>
                                  </div>
                                </v-col>
                                <v-col cols="6">
                                  <div class="text-caption text-grey mb-1">Đăng ký webinar</div>
                                  <div class="d-flex align-end">
                                    <span class="text-h6 font-weight-bold text-grey-darken-4">42</span>
                                    <v-chip size="x-small" color="green-lighten-4" text-color="green-darken-2" class="ml-2">
                                      ↑ 28%
                                    </v-chip>
                                  </div>
                                </v-col>
                              </v-row>
                              <div>
                                <div class="text-caption text-grey mb-1">Phản hồi tích cực</div>
                                <div class="d-flex align-center justify-space-between">
                                  <span class="text-body-2 font-weight-medium text-grey-darken-4">15 ứng viên đã phản hồi tích cực</span>
                                  <v-chip size="small" color="green-lighten-4" text-color="green-darken-2">Vượt mục tiêu</v-chip>
                                </div>
                              </div>
                            </div>
                          </v-card>
                          <v-card-text class="text-body-2 text-grey-darken-1 pa-0">
                            "Dựa trên phản hồi, tôi đề xuất tăng cường nội dung về công nghệ cloud và DevOps vì đây là chủ đề được quan tâm nhiều nhất. Tôi cũng đề xuất mở rộng chiến dịch thêm 2 tuần để tối ưu kết quả. Bạn có đồng ý không?"
                          </v-card-text>
                        </div>
                      </div>
                    </v-card>
                  </div>
                </v-card>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="d-flex justify-center ga-4 mt-10">
              <v-btn color="blue" size="large" variant="flat" class="px-8">
                Bắt đầu sử dụng
              </v-btn>
              <v-btn color="grey-lighten-1" size="large" variant="outlined" class="px-8">
                Tìm hiểu thêm
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>
  </v-container>
</template>

<script>
export default {
  name: 'ProductIntroduction',
  data() {
    return {
      // No reactive data needed for this static page
    }
  }
}
</script>

<style scoped>
.timeline-container {
  position: relative;
  padding-left: 40px;
}

.timeline-container::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: #e0e0e0;
}

.timeline-item {
  position: relative;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -30px;
  top: 12px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #1976d2;
  border: 3px solid #e3f2fd;
  z-index: 1;
}

.timeline-card {
  margin-left: 0;
}
</style> 