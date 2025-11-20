<template>
  <div class="min-h-screen bg-gray-50">
    <!-- <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
    </LayoutHeader> -->

    <div class="talent-detail-page w-full min-h-screen bg-gray-50">
      <!-- Loading State -->
      <Loading v-if="loading && !talent" text="Loading talent details..." />

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-8">
        <div class="text-red-600 mb-4">
          <FeatherIcon name="alert-circle" class="w-12 h-12 mx-auto" />
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">Error Loading Talent</h3>
        <p class="text-gray-600 mb-4">{{ error }}</p>
        <Button variant="outline" theme="blue" @click="handleRefresh">
          <template #prefix>
            <FeatherIcon name="refresh-cw" class="h-4 w-4" />
          </template>
          Try Again
        </Button>
      </div>

      <!-- Main Content -->
      <div v-else-if="talent" class="flex">
        <!-- Left Sidebar - Talent Information -->
        <div class="w-80 flex-shrink-0 bg-white border-r border-gray-200">
          <div class="sticky top-0 h-screen overflow-y-auto">
            <!-- Back Navigation -->
            <div class="p-4 border-gray-200">
              <button
                @click="goBack"
                class="flex items-center space-x-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                <FeatherIcon name="arrow-left" class="w-4 h-4" />
                <span class="font-medium">Back to Talent List</span>
              </button>
            </div>

            <!-- Talent Header -->
            <div class="p-6">
              <!-- Action Dropdown -->
              <div class="flex justify-end mb-4">
                <Dropdown :options="actionOptions" placement="bottom-end">
                  <template #default="{ open }">
                    <Button variant="ghost" theme="gray" class="p-2">
                      <FeatherIcon name="more-horizontal" class="w-4 h-4" />
                    </Button>
                  </template>
                </Dropdown>
              </div>

              <!-- Avatar and Basic Info -->
              <div class="text-center mb-6">
                <div class="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                  {{ getInitials(talent.full_name) }}
                </div>
                <h1 class="text-xl font-bold text-gray-900 mb-1">{{ talent.full_name }}</h1>
                <p class="text-gray-600 mb-2">{{ talent.email }}</p>
                <Badge v-if="talent.status" :theme="getStatusColor(talent.status)" variant="subtle">
                  {{ talent.status }}
                </Badge>
              </div>

              <!-- Contact Information -->
              <div class="space-y-4">
                <h3 class="text-sm font-medium text-gray-900 uppercase tracking-wide">Contact Information</h3>
                
                <div v-if="talent.phone" class="flex items-center space-x-3">
                  <FeatherIcon name="phone" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ talent.phone }}</span>
                </div>
                
                <div v-if="talent.email" class="flex items-center space-x-3">
                  <FeatherIcon name="mail" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ talent.email }}</span>
                </div>
                
                <div v-if="talent.location" class="flex items-center space-x-3">
                  <FeatherIcon name="map-pin" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ talent.location }}</span>
                </div>
              </div>

              <!-- Professional Information -->
              <div class="space-y-4 mt-6">
                <h3 class="text-sm font-medium text-gray-900 uppercase tracking-wide">Professional</h3>
                
                <!-- Resume Link -->
                <div v-if="talent.resume" class="flex items-center space-x-3">
                  <FeatherIcon name="file-text" class="w-4 h-4 text-gray-400 flex-shrink-0" />
                  <a 
                    :href="'/files/' + talent.resume" 
                    target="_blank" 
                    class="text-sm text-blue-600 hover:text-blue-800 hover:underline truncate"
                    :title="talent.resume"
                  >
                    {{ talent.resume }}
                  </a>
                </div>
                
                <div v-if="talent.position" class="flex items-center space-x-3">
                  <FeatherIcon name="briefcase" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ talent.position }}</span>
                </div>
                
                <div v-if="talent.current_city" class="flex items-center space-x-3">
                  <FeatherIcon name="map-pin" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ talent.current_city }}</span>
                </div>
                
                <div v-if="talent.latest_company" class="flex items-center space-x-3">
                  <FeatherIcon name="building" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ talent.latest_company }}</span>
                </div>
                
                <div v-if="talent.total_years_of_experience" class="flex items-center space-x-3">
                  <FeatherIcon name="clock" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ talent.total_years_of_experience }} years experience</span>
                </div>
              </div>


              <!-- Social Links -->
              <!-- <div class="space-y-4 mt-6">
                <h3 class="text-sm font-medium text-gray-900 uppercase tracking-wide">Social</h3>
                
                <div v-if="talent.linkedin_profile" class="flex items-center space-x-3">
                  <div class="flex items-center space-x-2">
                    <FeatherIcon name="linkedin" class="w-4 h-4 text-blue-600" />
                    <span class="text-sm text-gray-700">{{ talent.linkedin_profile }}</span>
                  </div>
                </div>
                
                <div v-if="talent.facebook_profile" class="flex items-center space-x-3">
                  <div class="flex items-center space-x-2">
                    <FeatherIcon name="facebook" class="w-4 h-4 text-blue-600" />
                    <span class="text-sm text-gray-700">{{ talent.facebook_profile }}</span>
                  </div>
                </div>
                
                <div v-if="talent.zalo_profile" class="flex items-center space-x-3">
                  <div class="flex items-center space-x-2">
                    <FeatherIcon name="message-circle" class="w-4 h-4 text-green-600" />
                    <span class="text-sm text-gray-700">{{ talent.zalo_profile }}</span>
                  </div>
                </div>
              </div> -->

              <!-- Tags -->
              <div class="mt-6">
                <TalentTagPicker
                  v-if="talent"
                  :docname="talent.name"
                  doctype="Mira Talent"
                  v-model="talent._user_tags"
                  :isTalentView="true"
                />
              </div>
            </div>

            <!-- Additional Information -->
            <div class="border-t border-gray-200">
              <div class="p-4">
                <h3 class="text-sm font-medium text-gray-900 mb-4 flex items-center">
                  <FeatherIcon name="info" class="w-4 h-4 mr-2" />
                  Additional Information
                </h3>
                
                <div class="space-y-3 text-sm">
                  <div v-if="talent.gender" class="flex justify-between">
                    <span class="text-gray-600">Gender:</span>
                    <span class="font-medium">{{ talent.gender }}</span>
                  </div>
                  <div v-if="talent.date_of_birth" class="flex justify-between">
                    <span class="text-gray-600">Date of Birth:</span>
                    <span class="font-medium">{{ formatDate(talent.date_of_birth) }}</span>
                  </div>
                  <div v-if="talent.experience_years" class="flex justify-between">
                    <span class="text-gray-600">Experience:</span>
                    <span class="font-medium">{{ formatExperience(talent.experience_years) }}</span>
                  </div>
                  <div v-if="talent.source" class="flex justify-between">
                    <span class="text-gray-600">Source:</span>
                    <span class="font-medium">{{ talent.source }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Created:</span>
                    <span class="font-medium">{{ formatDate(talent.creation) }}</span>
                  </div>
                  <div v-if="talent.recruitment_readiness" class="flex justify-between">
                    <span class="text-gray-600">Recruitment readiness:</span>
                    <span class="font-medium">{{ talent.recruitment_readiness }}</span>
                  </div>
                  <!-- <div v-if="talent.expected_salary" class="flex justify-between">
                    <span class="text-gray-600">Expected salary:</span>
                    <span class="font-medium">{{ formatCurrency(talent.expected_salary) }}</span>
                  </div> -->
                  <div v-if="talent.preferred_work_model" class="flex justify-between">
                    <span class="text-gray-600">Preferred work:</span>
                    <span class="font-medium">{{ talent.preferred_work_model }}</span>
                  </div>
                  <div v-if="talent.availability_date" class="flex justify-between">
                    <span class="text-gray-600">Availability date:</span>
                    <span class="font-medium">{{ formatDate(talent.availability_date) }}</span>
                  </div>
                </div>
              </div>

              <!-- Skills -->
              <div v-if="talent.skills" class="border-t border-gray-200 p-4">
                <h3 class="text-sm font-medium text-gray-900 mb-3 flex items-center">
                  <FeatherIcon name="zap" class="w-4 h-4 mr-2" />
                  Skills
                </h3>
                <div class="flex flex-wrap gap-2">
                  <Badge
                    v-for="skill in processSkills(talent.skills)"
                    :key="skill"
                    theme="blue"
                    variant="subtle"
                    class="text-xs"
                  >
                    {{ skill }}
                  </Badge>
                </div>
              </div>

              <!-- Social Profiles -->
              <div v-if="talent.linkedin_profile || talent.facebook_profile || talent.zalo_profile" class="border-t border-gray-200 p-4">
                <h3 class="text-sm font-medium text-gray-900 mb-3 flex items-center">
                  <FeatherIcon name="globe" class="w-4 h-4 mr-2" />
                  Social Profiles
                </h3>
                <div class="space-y-2">
                  <div v-if="talent.linkedin_profile" class="flex items-center space-x-2">
                    <FeatherIcon name="linkedin" class="w-4 h-4 text-blue-600" />
                    <a :href="talent.linkedin_profile" target="_blank" class="text-sm text-blue-600 hover:text-blue-800">
                      LinkedIn Profile
                    </a>
                  </div>
                  <div v-if="talent.facebook_profile" class="flex items-center space-x-2">
                    <FeatherIcon name="facebook" class="w-4 h-4 text-blue-600" />
                    <a :href="talent.facebook_profile" target="_blank" class="text-sm text-blue-600 hover:text-blue-800">
                      Facebook Profile
                    </a>
                  </div>
                  <div v-if="talent.zalo_profile" class="flex items-center space-x-2">
                    <FeatherIcon name="message-circle" class="w-4 h-4 text-green-600" />
                    <span class="text-sm text-gray-700">{{ talent.zalo_profile }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Content - Tabs -->
        <div class="flex-1 bg-white flex flex-col">
          <!-- Sticky Tab Navigation -->
          <div class="sticky top-0 z-10 bg-white border-b border-gray-200">
            <nav class="flex space-x-8 px-6" aria-label="Tabs">
              <button
                v-for="(tab, index) in tabs"
                :key="tab.name"
                @click="tabIndex = index"
                :class="[
                  'py-4 px-1 border-b-2 font-medium text-sm transition-colors flex items-center space-x-2',
                  tabIndex === index
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
              >
                <component :is="tab.icon" />
                <span>{{ tab.label }}</span>
                <Badge v-if="tab.count > 0" theme="gray" variant="subtle" class="text-xs">
                  {{ tab.count }}
                </Badge>
              </button>
            </nav>
          </div>

          <!-- Tab Content -->
          <div class="flex-1 overflow-y-auto">
            <div class="p-6">
              <div class="container mx-auto max-w-6xl">
                <!-- Summary Tab -->
                <TalentSummary v-if="tabs[tabIndex]?.content === 'summary'" :talent="talent" />
                
                <!-- Interactions Tab -->
                <TalentInteractions v-else-if="tabs[tabIndex]?.content === 'interactions'" :talent="talent" />
                
                <!-- Applications Tab -->
                <TalentApplications v-else-if="tabs[tabIndex]?.content === 'applications'" :talent="talent" />
                
                <!-- Activities Tab -->
                <TalentActivities v-else-if="tabs[tabIndex]?.content === 'activities'" :talent="talent" />
                
                <!-- Notes Tab -->
                <TalentNotes v-else-if="tabs[tabIndex]?.content === 'notes'" :talent="talent" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit Talent Dialog -->
  <Dialog
    v-model="showEditDialog"
    :options="{
      title: 'Edit Talent',
      size: '3xl',
    }"
  >
    <template #body-content>
      <form @submit.prevent="handleEditSubmit" class="space-y-4">
        <!-- Essential Information Section -->
        <div class="space-y-6">
          <h4 class="text-lg font-semibold text-gray-900 border-b border-gray-200 pb-3">
            {{ __('Essential Information') }}
          </h4>
          
          <!-- Row 1: Full Name and Gender -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Full Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Full Name <span class="text-red-500">*</span>
              </label>
              <input
                v-model="editForm.full_name"
                type="text"
                required
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                placeholder="Enter full name"
              />
            </div>

            <!-- Gender -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Gender
              </label>
              <select
                v-model="editForm.gender"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
              >
                <option value="">Select gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
                <option value="Unknown">Prefer not to say</option>
              </select>
            </div>
          </div>

          <!-- Row 2: Email and Phone -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Email Input -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Email <span class="text-red-500">*</span>
              </label>
              <input
                v-model="editForm.email"
                type="email"
                required
                @blur="checkEmail"
                :class="[
                  'block w-full rounded-md shadow-sm text-sm px-3 py-2',
                  emailError
                    ? 'border-red-300 text-red-900 placeholder-red-300 focus:border-red-500 focus:outline-none focus:ring-red-500'
                    : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500',
                ]"
                placeholder="Enter email address"
                aria-invalid="true"
                aria-describedby="email-error"
              />
              <p
                v-if="emailError"
                class="mt-1 text-xs text-red-600"
                id="email-error"
              >
                {{ emailError }}
              </p>
            </div>

            <!-- Phone -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Phone
              </label>
              <input
                v-model="editForm.phone"
                type="tel"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                placeholder="Enter phone number"
              />
            </div>
          </div>
        </div>

        <!-- Additional Information Section (Collapsible) -->
        <div class="border-t border-gray-200 pt-6">
          <button
            type="button"
            @click="showAdditionalInfo = !showAdditionalInfo"
            class="flex items-center justify-between w-full text-left text-lg font-semibold text-gray-900 hover:text-gray-700 focus:outline-none pb-3"
          >
            <span>{{ __('Additional Information') }}</span>
            <FeatherIcon 
              :name="showAdditionalInfo ? 'chevron-up' : 'chevron-down'" 
              class="h-5 w-5 transition-transform duration-200"
            />
          </button>
          
          <div v-show="showAdditionalInfo" class="mt-6 space-y-6">
            <!-- Social Media Profiles Section -->
            <div class="bg-gray-50 rounded-md p-3 space-y-3">
              <h5 class="text-sm font-medium text-gray-900 mb-2">Social Media Profiles</h5>
              
              <!-- LinkedIn and Facebook Row -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <!-- LinkedIn Profile -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    <div class="flex items-center">
                      <svg class="w-3 h-3 mr-1.5 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                      </svg>
                      LinkedIn
                    </div>
                  </label>
                  <input
                    v-model="editForm.linkedin_profile"
                    type="url"
                    class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                    placeholder="https://linkedin.com/in/username"
                  />
                </div>

                <!-- Facebook Profile -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    <div class="flex items-center">
                      <svg class="w-3 h-3 mr-1.5 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                      </svg>
                      Facebook
                    </div>
                  </label>
                  <input
                    v-model="editForm.facebook_profile"
                    type="url"
                    class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                    placeholder="https://facebook.com/username"
                  />
                </div>
              </div>

              <!-- Zalo Profile -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  <div class="flex items-center">
                    <svg class="w-3 h-3 mr-1.5 text-blue-500" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.568 8.16c-.169-.224-.487-.32-.75-.32-.487 0-.881.394-.881.881 0 .487.394.881.881.881.263 0 .581-.096.75-.32l.169-.224c.056-.075.094-.169.094-.263 0-.169-.075-.32-.169-.431-.056-.056-.094-.131-.094-.204zM12 18.72c-3.722 0-6.72-3.018-6.72-6.72S8.278 5.28 12 5.28s6.72 3.018 6.72 6.72-2.998 6.72-6.72 6.72z"/>
                    </svg>
                    Zalo
                  </div>
                </label>
                <input
                  v-model="editForm.zalo_profile"
                  type="text"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                  placeholder="Zalo username or phone number"
                />
              </div>
            </div>

            <!-- Skills Input -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Skills</label>
              <div>
                <div class="flex flex-wrap gap-1 mb-2" v-if="skillTags.length > 0">
                  <span
                    v-for="(skill, index) in skillTags"
                    :key="index"
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                  >
                    {{ skill }}
                    <button
                      type="button"
                      @click="removeSkill(index)"
                      class="ml-1 inline-flex text-blue-400 hover:text-blue-600 focus:outline-none"
                    >
                      <FeatherIcon name="x" class="h-3 w-3" />
                    </button>
                  </span>
                </div>
                <input
                  v-model="skillInput"
                  type="text"
                  placeholder="Type a skill and press Enter"
                  @keydown.enter.prevent="addSkill"
                  @blur="addSkill"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                />
              </div>
            </div>

            <!-- Two Column Layout for Company and Experience -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <!-- Latest Company -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Latest Company
                </label>
                <input
                  v-model="editForm.latest_company"
                  type="text"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                  placeholder="Company name"
                />
              </div>

              <!-- Total Years of Experience -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Years of Experience
                </label>
                <input
                  v-model.number="editForm.total_years_of_experience"
                  type="number"
                  min="0"
                  step="0.5"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                  placeholder="0"
                />
              </div>
            </div>

            <!-- Two Column Layout for Role and Source -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <!-- Desired Role -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Desired Role
                </label>
                <input
                  v-model="editForm.desired_role"
                  type="text"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                  placeholder="Enter desired role"
                />
              </div>

              <!-- Source -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Source</label>
                <select
                  v-model="editForm.source"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                >
                  <option
                    v-for="source in sourceOptions"
                    :key="source"
                    :value="source"
                  >
                    {{ source }}
                  </option>
                </select>
              </div>
            </div>

            <!-- Two Column Layout for Position and Current City -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <!-- Position -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Position
                </label>
                <input
                  v-model="editForm.position"
                  type="text"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                  placeholder="Enter current position"
                />
              </div>

              <!-- Current City -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Current City
                </label>
                <input
                  v-model="editForm.current_city"
                  type="text"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                  placeholder="Enter current city/address"
                />
              </div>
            </div>

            <!-- Status Fields -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <!-- Current Status -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Current Status</label>
                <select
                  v-model="editForm.current_status"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                >
                  <option value="Active">Active</option>
                  <option value="Passive">Passive</option>
                  <option value="Not Interested">Not Interested</option>
                  <option value="Hired">Hired</option>
                </select>
              </div>

              <!-- CRM Status -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">CRM Status</label>
                <select
                  v-model="editForm.crm_status"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                >
                  <option value="New">New</option>
                  <option value="Contacted">Contacted</option>
                  <option value="Qualified">Qualified</option>
                  <option value="Proposal">Proposal</option>
                  <option value="Negotiation">Negotiation</option>
                  <option value="Closed Won">Closed Won</option>
                  <option value="Closed Lost">Closed Lost</option>
                </select>
              </div>
            </div>

            <!-- Interaction Notes -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Interaction Notes
              </label>
              <textarea
                v-model="editForm.interaction_notes"
                rows="2"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3 py-2"
                placeholder="Add any notes from your interaction with this talent"
              ></textarea>
            </div>
          </div>
        </div>
      </form>
    </template>
    <template #actions>
      <div class="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          @click="showEditDialog = false"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Cancel
        </button>
        <button
          type="button"
          @click="handleEditSubmit"
          class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Update Talent
        </button>
      </div>
    </template>
  </Dialog>

</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTalentDetailStore } from '@/stores/talentDetail'
import { useTalentStore } from '@/stores/talent'
import { useToast } from '@/composables/useToast'
import { Button, Badge, Dropdown, FeatherIcon, Breadcrumbs, Tabs, Dialog, call } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Loading from '@/components/Loading.vue'
import TalentSummary from '@/components/talent/TalentSummary.vue'
import TalentInteractions from '@/components/talent/TalentInteractions.vue'
import TalentApplications from '@/components/talent/TalentApplications.vue'
import TalentActivities from '@/components/talent/TalentActivities.vue'
import TalentNotes from '@/components/talent/TalentNotes.vue'
import TalentTagPicker from '@/components/TalentTagPicker.vue'
import { useActiveTabManager } from "@/composables/useActiveTabManager";
// Router
const route = useRoute()
const router = useRouter()

// Store
const talentDetailStore = useTalentDetailStore()
const talentStore = useTalentStore()

// Composables
const { showSuccess, showError } = useToast()

// Helper for internationalization
const __ = (text) => text

// Reactive data
const talentName = computed(() => route.params.id)

// Computed from store
const talent = computed(() => talentDetailStore.talent)
const loading = computed(() => talentDetailStore.loading)
const error = computed(() => talentDetailStore.error)
const activities = computed(() => talentDetailStore.formattedActivities)
const attachments = computed(() => talentDetailStore.attachments)

// Computed for stats
const activityCount = computed(() => talentDetailStore.activityCount)
const commentCount = computed(() => talentDetailStore.commentCount)
const attachmentCount = computed(() => talentDetailStore.attachmentCount)

const recentActivities = computed(() => activities.value.slice(0, 5))

// Breadcrumbs
const breadcrumbs = computed(() => [
  { label: 'Talent', route: { name: 'Talent' } },
  { label: talent.value?.full_name || 'Detail', route: { name: 'TalentDetail', params: { id: talentName.value } } }
])

// Edit Dialog
const showEditDialog = ref(false)
const showAdditionalInfo = ref(false)
const editForm = ref({
  full_name: '',
  gender: '',
  email: '',
  phone: '',
  linkedin_profile: '',
  facebook_profile: '',
  zalo_profile: '',
  latest_company: '',
  total_years_of_experience: null,
  desired_role: '',
  source: 'Manually',
  position: '',
  current_city: '',
  interaction_notes: '',
  skills: [],
  current_status: 'Active',
  crm_status: 'New'
})

const sourceOptions = ref([
	'Manually',
	'Zalo',
	'Facebook',
	'LinkedIn',
	'Referral',
	'Headhunter',
	'Nurturing Interaction',
	'Import Excel',
  'Import CV',
  'MBW ATS'
])

const skillInput = ref('')
const skillTags = ref([])
const emailError = ref('')


// Main tabs configuration for Frappe UI Tabs
const tabs = computed(() => [
  {
    label: 'Summary',
    name: 'summary',
    icon: h(FeatherIcon, { class: 'w-4 h-4', name: 'bar-chart-2' }),
    count: 0,
    content: 'summary'
  },
  {
    label: 'Interactions',
    name: 'interactions',
    icon: h(FeatherIcon, { class: 'w-4 h-4', name: 'users' }),
    count: 0,
    content: 'interactions'
  },
  {
    label: 'Applications',
    name: 'applications',
    icon: h(FeatherIcon, { class: 'w-4 h-4', name: 'briefcase' }),
    count: 0,
    content: 'applications'
  },
  {
    label: 'Activities',
    name: 'activities',
    icon: h(FeatherIcon, { class: 'w-4 h-4', name: 'activity' }),
    count: activityCount.value,
    content: 'activities'
  },
  {
    label: 'Notes',
    name: 'notes',
    icon: h(FeatherIcon, { class: 'w-4 h-4', name: 'message-circle' }),
    count: commentCount.value,
    content: 'notes'
  }
])

// Tab index for custom tabs
const tabIndex = ref(0)


// Action dropdown options
const actionOptions = [
  {
    label: 'Edit Talent',
    icon: 'edit',
    onClick: () => editTalent()
  },
  {
    label: 'Delete Talent',
    icon: 'trash-2',
    onClick: () => deleteTalent(),
    class: 'text-red-600'
  }
]

// Methods
const handleRefresh = async () => {
  await talentDetailStore.fetchTalent(talentName.value)
}

const goBack = () => {
  router.push({ name: 'TalentPool' })
}


const editTalent = () => {
  if (talent.value) {
    // Debug log to see what data we have
    console.log('Current talent data:', talent.value)
    console.log('Talent position:', talent.value.position)
    console.log('Talent current_city:', talent.value.current_city)
    
    // Populate form with current talent data - handle all possible field names
    editForm.value = {
      full_name: talent.value.full_name || talent.value.name || '',
      gender: talent.value.gender || '',
      email: talent.value.email || '',
      phone: talent.value.phone || talent.value.mobile_no || '',
      linkedin_profile: talent.value.linkedin_profile || '',
      facebook_profile: talent.value.facebook_profile || '',
      zalo_profile: talent.value.zalo_profile || '',
      latest_company: talent.value.latest_company || talent.value.company || '',
      total_years_of_experience: talent.value.total_years_of_experience || talent.value.experience_years || null,
      desired_role: talent.value.desired_role || talent.value.role || '',
      source: talent.value.source || talent.value.talent_source || 'Manually',
      position: talent.value.position || '',
      current_city: talent.value.current_city || '',
      interaction_notes: talent.value.interaction_notes || talent.value.notes || '',
      skills: (() => {
        console.log('Raw skills data:', talent.value.skills)
        const processed = processSkills(talent.value.skills) || []
        console.log('Processed skills:', processed)
        return processed
      })(),
      current_status: talent.value.current_status || talent.value.status || 'Active',
      crm_status: talent.value.crm_status || 'New'
    }
    
    // Set skill tags for display
    skillTags.value = [...editForm.value.skills]
    
    // Reset additional info section to closed
    showAdditionalInfo.value = false
    
    // Clear any previous errors
    emailError.value = ''
    
    // Open dialog
    showEditDialog.value = true
    
    console.log('Populated edit form:', editForm.value)
  }
}

const deleteTalent = () => {
  // TODO: Implement delete functionality
  showError('Delete functionality coming soon')
}

const downloadAttachment = (attachment) => {
  window.open(attachment.file_url, '_blank')
}

// Edit form helper functions
const addSkill = () => {
  const skill = skillInput.value.trim()
  if (skill && !skillTags.value.includes(skill)) {
    skillTags.value.push(skill)
    editForm.value.skills = [...skillTags.value]
    skillInput.value = ''
  }
}

const removeSkill = (index) => {
  skillTags.value.splice(index, 1)
  editForm.value.skills = [...skillTags.value]
}

const checkEmail = () => {
  const email = editForm.value.email
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    emailError.value = 'Please enter a valid email address'
  } else {
    emailError.value = ''
  }
}

const handleEditSubmit = async () => {
  try {
    // Validate required fields
    if (!editForm.value.full_name.trim()) {
      showError('Full name is required')
      return
    }
    
    if (!editForm.value.email.trim()) {
      showError('Email is required')
      return
    }
    
    // Check email format
    checkEmail()
    if (emailError.value) {
      return
    }
    
    // Prepare data for API
    console.log('Skills before processing:', editForm.value.skills)
    
    // Convert skills array to comma-separated string for storage
    const skillsString = editForm.value.skills.length > 0 
      ? editForm.value.skills.join(', ') 
      : ''
    
    const updateData = {
      ...editForm.value,
      skills: skillsString // Send as comma-separated string
    }
    console.log('Update data being sent:', updateData)
    
    // Call store method to update talent
    const result = await talentStore.updateTalent(talentName.value, updateData)
    
    if (!result.success) {
      throw new Error(result.message || result.error || 'Failed to update talent')
    }
    
    // Close dialog and refresh data
    showEditDialog.value = false
    await handleRefresh()
    
    showSuccess('Talent updated successfully')
  } catch (error) {
    console.error('Error updating talent:', error)
    showError('Failed to update talent')
  }
}

// Helper methods
const getInitials = (name) => {
  if (!name) return 'T'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const getStatusColor = (status) => {
  switch (status) {
    case 'Active': return 'green'
    case 'Passive': return 'yellow'
    case 'Not Interested': return 'red'
    case 'Hired': return 'blue'
    default: return 'gray'
  }
}

const processSkills = (skillsStr) => {
  if (!skillsStr) return []
  
  // If it's already an array, return it
  if (Array.isArray(skillsStr)) {
    return skillsStr.map(skill => String(skill).trim()).filter(skill => skill.length > 0)
  }
  
  // Convert to string if it's not
  const str = String(skillsStr).trim()
  console.log('Processing skills string:', str)
  
  // Try to parse as JSON first (for cases like '["skill1","skill2"]')
  try {
    const parsed = JSON.parse(str)
    if (Array.isArray(parsed)) {
      console.log('Parsed as JSON array:', parsed)
      return parsed.map(skill => String(skill).trim()).filter(skill => skill.length > 0)
    }
  } catch (e) {
    // Continue to manual parsing
  }
  
  // Handle string format like '[\"skill1\",\"skill2\"]' (escaped JSON)
  if (str.startsWith('[') && str.endsWith(']')) {
    try {
      const content = str.slice(1, -1) // Remove [ and ]
      if (!content.trim()) return []
      
      const items = content.split(',').map(item => {
        // Remove quotes and whitespace: "skill" -> skill
        return item.trim().replace(/^["']|["']$/g, '').replace(/\\"/g, '"')
      }).filter(item => item.length > 0)
      
      console.log('Parsed as bracket format:', items)
      return items
    } catch (e) {
      console.warn('Failed to parse skills array format:', str)
    }
  }
  
  // Handle comma-separated string (most common case)
  const result = str.split(',').map(skill => skill.trim()).filter(skill => skill.length > 0)
  console.log('Parsed as comma-separated:', result)
  return result
}

const processTags = (tagsStr) => {
  if (!tagsStr) return []
  return tagsStr.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0)
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  } catch (error) {
    return dateStr
  }
}

const formatExperience = (years) => {
  if (!years) return '-'
  const num = parseFloat(years)
  if (num === 1) return '1 year'
  return `${num} years`
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const getActivityDotColor = (type) => {
  switch (type) {
    case 'comment': return 'bg-blue-500'
    case 'changed': return 'bg-yellow-500'
    case 'added': return 'bg-green-500'
    case 'removed': return 'bg-red-500'
    case 'creation': return 'bg-purple-500'
    default: return 'bg-gray-500'
  }
}

const getActivitySummary = (activity) => {
  switch (activity.activity_type) {
    case 'comment': return 'Added a comment'
    case 'changed': return `Changed ${activity.data.field_label}`
    case 'added': return `Added ${activity.data.field_label}`
    case 'removed': return `Removed ${activity.data.field_label}`
    case 'creation': return 'Created this talent'
    default: return activity.activity_type
  }
}

// Lifecycle
onMounted(async () => {
  if (talentName.value) {
    await talentDetailStore.fetchTalent(talentName.value)
  }
})

// Watch for route changes
watch(() => route.params.id, async (newId) => {
  if (newId) {
    talentDetailStore.clearTalent()
    await talentDetailStore.fetchTalent(newId)
  }
})

// Cleanup on unmount
onUnmounted(() => {
  talentDetailStore.clearTalent()
})
</script>

<style scoped>
/* Layout */
.talent-detail-page {
  height: calc(100vh - 60px); /* Adjust based on header height */
}

/* Custom scrollbar for sidebar */
.talent-detail-page ::-webkit-scrollbar {
  width: 6px;
}

.talent-detail-page ::-webkit-scrollbar-track {
  background: #f8fafc;
}

.talent-detail-page ::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.talent-detail-page ::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Sidebar styling */
.talent-detail-page .w-80 {
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.05);
}

/* Tab content container */
.talent-detail-page .container {
  padding-left: 0;
  padding-right: 0;
}

/* Smooth transitions */
.talent-detail-page button {
  transition: all 0.2s ease-in-out;
}

/* Loading animation */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .talent-detail-page .w-80 {
    width: 280px;
  }
}

@media (max-width: 768px) {
  .talent-detail-page .flex {
    flex-direction: column;
  }
  
  .talent-detail-page .w-80 {
    width: 100%;
    height: auto;
    position: relative;
  }
  
  .talent-detail-page .sticky {
    position: relative;
    height: auto;
  }
}
</style>
