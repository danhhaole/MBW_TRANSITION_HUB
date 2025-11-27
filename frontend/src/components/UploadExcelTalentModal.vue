<template>
    <Dialog v-model="internalShow" :options="{ size: '5xl' }">
        <template #body-title>{{ __("Upload Talent") }}</template>
        <template #body-content>
            <!-- Header với Progress Steps -->
            <div class="flex items-center justify-between p-5 border-b">
                <div class="flex-1">
                    <!-- <h3 class="text-xl font-semibold mb-3"></h3> -->
                    <!-- Progress Steps -->
                    <div class="flex items-center space-x-4">
                        <div v-for="(step, index) in steps" :key="step.key" class="flex items-center"
                            :class="{ 'opacity-50': !isStepAccessible(step.key) }">

                            <!-- Step Circle -->
                            <div class="flex items-center justify-center w-8 h-8 rounded-full border-2 text-sm font-medium"
                                :class="getStepCircleClass(step.key)">
                                <span v-if="isStepCompleted(step.key)">✓</span>
                                <span v-else>{{ index + 1 }}</span>
                            </div>

                            <!-- Step Label -->
                            <span class="ml-2 text-sm font-medium" :class="getStepTextClass(step.key)">
                                {{ __(step.label) }}
                            </span>

                            <!-- Connector Line -->
                            <div v-if="index < steps.length - 1" class="w-12 h-0.5 mx-4"
                                :class="isStepCompleted(step.key) ? 'bg-blue-500' : 'bg-gray-300'">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- <Button variant="ghost" @click="closeModal">
                    <FeatherIcon name="x" class="h-4 w-4" />
                </Button> -->
            </div>

            <div class="candidate-uploader">
                <!-- Step 1: Template & Setup -->
                <div v-if="currentStep === 'upload'" class="step-content">
                    <div class="step-header">
                        <h4 class="step-title">{{ __("Step 1: Prepare Your Data") }}</h4>
                        <p class="step-description">{{ __("Download the template and prepare your talent data") }}
                        </p>
                    </div>

                    <!-- Template Download Section -->
                    <div class="card mb-6">
                        <div class="card-header">
                            <div class="flex items-center">
                                <div class="icon-circle bg-blue-100 text-blue-600 mr-3">
                                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                </div>
                                <div class="flex-1">
                                    <h5 class="card-title">{{ __('Download Template') }}</h5>
                                    <p class="card-subtitle">{{ __("Get the correct format for your data") }}</p>
                                </div>
                                <button class="btn btn-outline btn-sm" @click="downloadTemplate"
                                    :disabled="isDownloading">
                                    <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                    {{ isDownloading ? __('Downloading...') : __('Download') }}
                                </button>
                            </div>
                        </div>
                        <!-- <div class="card-body">
                            <p class="text-sm text-gray-600">
                                {{ __("Download the sample template to ensure your data is formatted correctly before uploading.")}}
                            </p>
                        </div> -->
                    </div>

                    <!-- Job Selection -->
                    <div class="card mb-6">
                        <div class="card-header">
                            <div class="flex items-center">
                                <div class="icon-circle bg-green-100 text-green-600 mr-3">
                                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2M8 6v6a2 2 0 002 2h4a2 2 0 002-2V6" />
                                    </svg>
                                </div>
                                <div>
                                    <h5 class="card-title">{{ __("Select Segment") }}</h5>
                                    <p class="card-subtitle">{{ __("Link segment to a specific (optional)") }}
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="card-body">
                            <Link :doctype="'Mira Segment'" v-model="selectedJob"
                                :placeholder="__('Select segment')" />
                        </div>
                    </div>

                    <!-- Upload Area -->
                    <div class="card">
                        <div class="card-header">
                            <div class="flex items-center">
                                <div class="icon-circle bg-purple-100 text-purple-600 mr-3">
                                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                    </svg>
                                </div>
                                <div>
                                    <h5 class="card-title">{{ __("Upload Your File") }}</h5>
                                    <p class="card-subtitle">{{ __("Drop your Excel or CSV file here") }}</p>
                                </div>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="drop-zone" :class="{ 'drag-over': isDragOver }" @drop="handleDrop"
                                @dragover.prevent="isDragOver = true" @dragleave.prevent="isDragOver = false"
                                @dragenter.prevent>
                                <div class="text-center p-8">
                                    <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" stroke="currentColor" fill="none"
                                        viewBox="0 0 48 48">
                                        <path
                                            d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                                            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                                    </svg>
                                    <p class="text-xl font-medium text-gray-900 mb-2">{{ __("Drop files here or click to upload")}}</p>
                                    <p class="text-sm text-gray-500 mb-4">{{ __("Support Excel (.xlsx, .xls) and CSV files") }}</p>
                                    <input ref="fileInput" type="file" class="hidden" accept=".xlsx,.xls,.csv"
                                        @change="handleFileSelect">
                                    <button class="btn btn-primary btn-lg" @click="$refs.fileInput.click()">
                                        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                        </svg>
                                        {{ __("Select File") }}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Step 2: Processing -->
                <div v-if="currentStep === 'processing'" class="step-content">
                    <div class="step-header">
                        <h4 class="step-title">{{ __("Step 2: Processing File") }}</h4>
                        <p class="step-description">{{ __("Analyzing your job openings file and extracting data") }}</p>
                    </div>

                    <div class="card">
                        <div class="card-body text-center py-12">
                            <div class="spinner mb-6"></div>
                            <h5 class="text-lg font-medium mb-2">{{ __("Processing file...") }}</h5>
                            <p class="text-gray-500">{{ __("Please wait while we analyze your file") }}</p>
                        </div>
                    </div>
                </div>

                <!-- Step 3: Preview & Mapping -->
                <div v-if="currentStep === 'mapping'" class="step-content">
                    <div class="step-header">
                        <h4 class="step-title">{{ __("Step 3: Review and Map Fields") }}</h4>
                        <p class="step-description">{{ __("Review your data and map columns to job opening fields") }}
                        </p>
                        <button class="btn btn-outline mt-4" @click="goBackToUpload">
                            <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M15 19l-7-7 7-7" />
                            </svg>
                            {{ __("Back to Upload") }}
                        </button>
                    </div>

                    <!-- File Info Card -->
                    <div class="card mb-6">
                        <div class="card-header">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center">
                                    <div class="icon-circle bg-green-100 text-green-600 mr-3">
                                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                    </div>
                                    <div>
                                        <h5 class="card-title">{{ previewData.filename }}</h5>
                                        <p class="card-subtitle">{{ previewData.total_rows }} {{ __("records found") }}
                                        </p>
                                    </div>
                                </div>
                                <button class="btn btn-outline btn-sm" @click="goBackToUpload">
                                    {{ __("Upload Different File") }}
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Sample Data Preview -->
                    <div class="card mb-6">
                        <div class="card-header">
                            <h5 class="card-title">{{ __("Sample Data Preview") }}</h5>
                            <p class="card-subtitle">{{ __("First few rows from your file") }}</p>
                        </div>
                        <div class="card-body">
                            <div class="overflow-x-auto max-h-64 border rounded-lg">
                                <table class="min-w-full border-collapse">
                                    <thead class="bg-gray-50 sticky top-0">
                                        <tr>
                                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                                                #</th>
                                            <th v-for="column in previewData.columns" :key="column"
                                                class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase border-l">
                                                {{ column }}
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(row, index) in previewData.sample" :key="index"
                                            class="hover:bg-gray-50">
                                            <td class="px-4 py-2 text-sm font-medium text-gray-900 border-b">{{ index +
                                                1 }}</td>
                                            <td v-for="column in previewData.columns" :key="column"
                                                class="px-4 py-2 text-sm text-gray-900 border-b border-l max-w-xs truncate"
                                                :title="row[column]">
                                                {{ row[column] || '-' }}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- Field Mapping -->
                    <div class="card mb-6">
                        <div class="card-header">
                            <div class="flex items-center justify-between">
                                <div>
                                    <h5 class="card-title">{{ __("Field Mapping") }}</h5>
                                    <p class="card-subtitle">{{ __("Map your file columns to job opening fields") }}</p>
                                </div>
                                <div class="flex space-x-2">
                                    <button class="btn btn-outline btn-sm" @click="autoMapFields">
                                        <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M13 10V3L4 14h7v7l9-11h-7z" />
                                        </svg>
                                        {{ __("Auto Map") }}
                                    </button>
                                    <button class="btn btn-outline btn-sm" @click="clearMapping">
                                        <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M6 18L18 6M6 6l12 12" />
                                        </svg>
                                        {{ __("Clear All") }}
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="mapping-grid">
                                <div v-for="field in availableFields" :key="field.fieldname" class="mapping-field">
                                    <label class="block text-sm font-medium text-gray-700 mb-2">
                                        {{ field.label }}
                                        <span v-if="field.reqd" class="text-red-500 ml-1">*</span>
                                    </label>
                                    <select v-model="fieldMapping[field.fieldname]"
                                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                                        :class="{ 'border-red-500 ring-red-500': field.reqd && !fieldMapping[field.fieldname] }">
                                        <option value="">{{ __("-- Select Column --") }}</option>
                                        <option v-for="column in previewData.columns" :key="column" :value="column">
                                            {{ column }}
                                        </option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Import Options -->
                    <div class="card mb-6">
                        <div class="card-header">
                            <h5 class="card-title">{{ __("Import Options") }}</h5>
                            <p class="card-subtitle">{{ __("Configure how data should be imported") }}</p>
                        </div>
                        <div class="card-body">
                            <div class="space-y-3">
                                <label class="flex items-center">
                                    <input type="checkbox" v-model="validateOnly"
                                        class="form-checkbox h-4 w-4 text-blue-600 rounded">
                                    <span class="ml-3 text-sm text-gray-700">{{ __("Validate only (don't import data)")
                                        }}</span>
                                </label>
                                <label class="flex items-center">
                                    <input type="checkbox" v-model="skipDuplicates"
                                        class="form-checkbox h-4 w-4 text-blue-600 rounded">
                                    <span class="ml-3 text-sm text-gray-700">{{ __("Skip duplicate emails") }}</span>
                                </label>
                            </div>
                        </div>
                    </div>

                    <!-- Validation Issues -->
                    <div v-if="validationIssues.length > 0" class="alert alert-warning mb-6">
                        <div class="flex items-start">
                            <svg class="h-5 w-5 text-yellow-400 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                            </svg>
                            <div class="ml-3">
                                <h6 class="text-sm font-medium text-yellow-800">{{ __('Mapping Issues') }}</h6>
                                <div class="mt-2 text-sm text-yellow-700">
                                    <ul class="list-disc list-inside space-y-1">
                                        <li v-for="issue in validationIssues" :key="issue">{{ issue }}</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Step Navigation -->
                    <div class="flex justify-end">
                        <div class="flex space-x-3">
                            <button v-if="canProcess" class="btn btn-outline" @click="validateData"
                                :disabled="isValidating">
                                <span v-if="isValidating" class="inline-block animate-spin mr-2">⌛</span>
                                <svg v-else class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                {{ isValidating ? __("Validating...") : __("Validate Data") }}
                            </button>
                            <button class="btn btn-primary" @click="processImport"
                                :disabled="!canProcess || isImporting">
                                <span v-if="isImporting" class="inline-block animate-spin mr-2">⌛</span>
                                <svg v-else class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                                </svg>
                                {{ isImporting ? __("Importing...") : (validateOnly ? __("Validate") : __("Import Data")) }}
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Step 4: Import Progress -->
                <div v-if="currentStep === 'importing'" class="step-content">
                    <div class="step-header">
                        <h4 class="step-title">{{ __("Step 4: Importing Data") }}</h4>
                        <p class="step-description">{{ __("Processing and importing your job opening data") }}</p>
                    </div>

                    <div class="card">
                        <div class="card-body text-center py-12">
                            <div class="progress-spinner mb-6"></div>
                            <h5 class="text-xl font-medium mb-3">{{ __("Importing Data") }}</h5>
                            <p class="text-gray-600 mb-8">{{ __("Please wait while we process your data...") }}</p>

                            <!-- Progress Bar -->
                            <div v-if="importProgress" class="max-w-md mx-auto">
                                <div class="flex justify-between items-center mb-2">
                                    <span class="text-sm font-medium">{{ __("Progress") }}</span>
                                    <span class="text-sm text-gray-500">
                                        {{ importProgress.processed }} / {{ importProgress.total }}
                                    </span>
                                </div>
                                <div class="w-full bg-gray-200 rounded-full h-3">
                                    <div class="bg-blue-600 h-3 rounded-full transition-all duration-500"
                                        :style="{ width: `${(importProgress.processed / importProgress.total) * 100}%` }">
                                    </div>
                                </div>
                                <div class="flex justify-between text-sm text-gray-500 mt-2">
                                    <span>{{ importProgress.success }} {{ __("successful") }}</span>
                                    <span>{{ importProgress.failed }} {{ __("failed") }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Step 5: Results -->
                <div v-if="currentStep === 'results'" class="step-content">
                    <div class="step-header">
                        <h4 class="step-title">
                            {{ validateOnly ? __("Step 4: Validation Results") : __("Step 5: Import Results") }}
                        </h4>
                        <p class="step-description">
                            {{ validateOnly ? __("Review validation results") : __("Review import results and next steps") }}
                        </p>
                    </div>

                    <!-- Results Summary -->
                    <div class="card mb-6">
                        <div class="card-header">
                            <h5 class="card-title">
                                {{ validateOnly ? __("Validation Summary") : __("Import Summary") }}
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div class="stat-card success">
                                    <div class="stat-value">{{ importResults.success }}</div>
                                    <div class="stat-label">{{ validateOnly ? __("Valid Records") : __("Successfully Imported") }}</div>
                                </div>
                                <div class="stat-card error">
                                    <div class="stat-value">{{ importResults.failed }}</div>
                                    <div class="stat-label">{{ validateOnly ? __("Invalid Records") : __("Failed to Import") }}</div>
                                </div>
                                <div class="stat-card total">
                                    <div class="stat-value">{{ importResults.total }}</div>
                                    <div class="stat-label">{{ __("Total Records") }}</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Detailed Log -->
                    <div v-if="importResults.logs && importResults.logs.length > 0" class="card mb-6">
                        <div class="card-header">
                            <div class="flex items-center justify-between">
                                <div>
                                    <h5 class="card-title">{{ __("Detailed Log") }}</h5>
                                    <p class="card-subtitle">{{ __("See what happened with each record") }}</p>
                                </div>
                                <select v-model="logFilter" class="px-3 py-1 border rounded-md text-sm">
                                    <option value="all">{{ __("All Records") }}</option>
                                    <option value="success">{{ __("Success Only") }}</option>
                                    <option value="error">{{ __("Errors Only") }}</option>
                                </select>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="max-h-96 overflow-y-auto space-y-2">
                                <div v-for="(log, index) in filteredLogs" :key="index" class="log-entry"
                                    :class="getLogEntryClass(log.status)">
                                    <div class="flex justify-between items-start">
                                        <div class="flex-1">
                                            <div class="font-medium text-sm">
                                                {{ __("Row") }} {{ log.row_number }}: {{ log.full_name || 'Unknown' }}
                                            </div>
                                            <div class="text-sm text-gray-600 mt-1">{{ log.message }}</div>
                                        </div>
                                        <span class="status-badge" :class="getStatusBadgeClass(log.status)">
                                            {{ log.status.toUpperCase() }}
                                        </span>
                                    </div>
                                </div>
                                <div v-if="filteredLogs.length === 0" class="text-center text-gray-500 py-4">
                                    {{ __("No logs match the current filter") }}
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Final Actions -->
                    <div class="flex justify-between">
                        <button class="btn btn-outline" @click="resetUpload">
                            <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                            </svg>
                            {{ __("Import Another File") }}
                        </button>
                        <div class="flex space-x-3">
                            <button v-if="importResults.failed > 0" class="btn btn-outline" @click="downloadErrorLog">
                                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                                {{ __("Download Error Log") }}
                            </button>
                            <button v-if="validateOnly && importResults.success > 0" class="btn btn-success"
                                @click="proceedWithImport">
                                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                {{ __("Proceed with Import") }}
                            </button>
                            <button v-if="!validateOnly && importResults.success > 0" class="btn btn-primary"
                                @click="goToTalentList">
                                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                                </svg>
                                {{ __("View Talent") }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </Dialog>

    <!-- Import History Modal -->
    <Dialog v-model="showImportHistory" :options="{ size: '4xl' }">
        <template #body>
            <div class="flex items-center justify-between p-5 border-b">
                <h3 class="text-xl font-semibold">{{ __("Import History") }}</h3>
                <Button variant="ghost" @click="showImportHistory = false">
                    <FeatherIcon name="x" class="h-4 w-4" />
                </Button>
            </div>

            <div class="p-6">
                <div v-if="loadingHistory" class="text-center py-8">
                    <div class="spinner mb-4"></div>
                    <p>{{ __("Loading import history...") }}</p>
                </div>

                <div v-else-if="importHistory.length === 0" class="text-center py-8 text-gray-500">
                    <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <p>{{ __("No import history found") }}</p>
                </div>

                <div v-else class="space-y-4">
                    <div v-for="session in importHistory" :key="session.name"
                        class="border rounded-lg p-4 hover:bg-gray-50">
                        <div class="flex justify-between items-start mb-3">
                            <div class="flex-1">
                                <div class="flex items-center space-x-2 mb-1">
                                    <h4 class="font-medium">{{ session.file_name }}</h4>
                                    <span v-if="session.is_retry"
                                        class="px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded-full">{{
                                        __("RETRY") }}</span>
                                </div>
                                <p class="text-sm text-gray-600">{{ __("By") }} {{ session.created_by }} • {{
                                    formatDate(session.started_at) }}</p>
                                <p v-if="session.candidate" class="text-sm text-blue-600">{{ __("Job:") }} {{
                                    session.candidate }}</p>
                            </div>
                            <span class="status-badge" :class="getSessionStatusClass(session.status)">{{ session.status
                                }}</span>
                        </div>

                        <div class="grid grid-cols-4 gap-4 text-sm mb-3">
                            <div class="text-center">
                                <div class="font-medium text-gray-900">{{ session.total_rows }}</div>
                                <div class="text-gray-500">{{ __("Total") }}</div>
                            </div>
                            <div class="text-center">
                                <div class="font-medium text-green-600">{{ session.success_count || 0 }}</div>
                                <div class="text-gray-500">{{ __("Success") }}</div>
                            </div>
                            <div class="text-center">
                                <div class="font-medium text-red-600">{{ session.failed_count || 0 }}</div>
                                <div class="text-gray-500">{{ __("Failed") }}</div>
                            </div>
                            <div class="text-center">
                                <div class="font-medium text-orange-600">{{ session.retry_job_openings || 0 }}</div>
                                <div class="text-gray-500">{{ __("Can Retry") }}</div>
                            </div>
                        </div>

                        <div class="flex justify-between items-center">
                            <div class="text-sm text-gray-500">{{ session.error_summary || __("No errors") }}</div>
                            <div class="flex space-x-2">
                                <button v-if="session.can_retry && session.retry_job_openings > 0"
                                    class="btn btn-outline btn-sm" @click="retrySession(session.name)"
                                    :disabled="retryingSessions.includes(session.name)">
                                    <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                    </svg>
                                    {{ retryingSessions.includes(session.name) ? __("Retrying...") : __("Retry") }}
                                </button>
                                <button class="btn btn-outline btn-sm" @click="viewSessionDetails(session.name)">
                                    <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                    </svg>
                                    {{ __("Details") }}
                                </button>
                                <button v-if="session.status !== 'Processing'"
                                    class="btn btn-outline btn-sm text-red-600 border-red-300 hover:bg-red-50"
                                    @click="deleteSession(session.name)">
                                    <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                    </svg>
                                    {{ __("Delete") }}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="flex justify-center mt-6">
                    <button class="btn btn-outline" @click="refreshImportHistory">
                        <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        {{ __("Refresh") }}
                    </button>
                </div>
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { call } from 'frappe-ui'
import { useRouter } from 'vue-router'
import { globalStore } from '@/stores/global';
import { useToast } from '@/composables/useToast'

const { $socket } = globalStore();
const router = useRouter()
const toast = useToast()

// Props and emits
const props = defineProps({
    modelValue: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue', 'created', 'close'])

const internalShow = computed({
  get() {
    return props.modelValue
  },
  set(value) {
    emit('update:modelValue', value)
  }
})

// Steps configuration
const steps = ref([
    { key: 'upload', label: 'Prepare & Upload' },
    { key: 'processing', label: 'Processing' },
    { key: 'mapping', label: 'Review & Map' },
    { key: 'importing', label: 'Importing' },
    { key: 'results', label: 'Results' }
])

// Reactive state
const currentStep = ref('upload')
const isDragOver = ref(false)
const isDownloading = ref(false)
const isValidating = ref(false)
const isImporting = ref(false)
const selectedJob = ref(null)
const selectedFile = ref(null)
const previewData = ref(null)
const availableFields = ref([])
const fieldMapping = ref({})
const validateOnly = ref(false)
const skipDuplicates = ref(true)
const importResults = ref(null)
const importProgress = ref(null)
const sessionId = ref(null)
const logFilter = ref('all')

// Import History
const showImportHistory = ref(false)
const importHistory = ref([])
const loadingHistory = ref(false)
const retryingSessions = ref([])

// Real-time updates
let progressInterval = null

// Computed properties
const show = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
})

const canProcess = computed(() => {
    if (!previewData.value || !availableFields.value.length) return false

    const requiredMapped = availableFields.value
        .filter(field => field.reqd)
        .every(field => fieldMapping.value[field.fieldname])

    return requiredMapped
})

const validationIssues = computed(() => {
    const issues = []
    if (!availableFields.value.length) return issues

    availableFields.value
        .filter(field => field.reqd)
        .forEach(field => {
            if (!fieldMapping.value[field.fieldname]) {
                issues.push(__(`Required field "${field.label}" is not mapped`))
            }
        })
    return issues
})

const filteredLogs = computed(() => {
    if (!importResults.value?.logs) return []

    if (logFilter.value === 'all') return importResults.value.logs
    return importResults.value.logs.filter(log => log.status === logFilter.value)
})

// Step helper methods
const isStepAccessible = (stepKey) => {
    const stepIndex = steps.value.findIndex(s => s.key === stepKey)
    const currentIndex = steps.value.findIndex(s => s.key === currentStep.value)
    return stepIndex <= currentIndex
}

const isStepCompleted = (stepKey) => {
    const stepIndex = steps.value.findIndex(s => s.key === stepKey)
    const currentIndex = steps.value.findIndex(s => s.key === currentStep.value)
    return stepIndex < currentIndex
}

const getStepCircleClass = (stepKey) => {
    if (isStepCompleted(stepKey)) {
        return 'bg-blue-600 border-blue-600 text-white'
    } else if (stepKey === currentStep.value) {
        return 'bg-blue-100 border-blue-600 text-blue-600'
    } else {
        return 'bg-gray-100 border-gray-300 text-gray-500'
    }
}

const getStepTextClass = (stepKey) => {
    if (isStepCompleted(stepKey) || stepKey === currentStep.value) {
        return 'text-blue-600'
    } else {
        return 'text-gray-500'
    }
}

// Watch for modal close to reset state
watch(show, (newVal) => {
    if (!newVal) {
        resetUpload()
        stopProgressTracking()
    }
})

onMounted(() => {
    if ($socket && typeof $socket.on === 'function') {
        $socket.on('import_progress', (data) => {
            if (data.session_id) {
                handleProgressUpdate(data)
            }
        })
    }
})

onUnmounted(() => {
    stopProgressTracking()
    if ($socket && typeof $socket.off === 'function') {
        $socket.off('import_progress', handleProgressUpdate)
    }
})

// Template download ( thêm api )
const downloadTemplate = async () => {
    isDownloading.value = true
    try {
        const response = await call('mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.download_talent_template')

        if (response.file_url) {
            const link = document.createElement('a')
            link.href = response.file_url
            link.download = response.file_name || 'talent_import_template.xlsx'
            link.target = '_blank'
            link.style.display = 'none'

            document.body.appendChild(link)
            link.click()

            setTimeout(() => {
                document.body.removeChild(link)
            }, 100)
        } else {
            throw new Error('No file URL returned from server')
        }

        toast.success(__('Template has been downloaded successfully.'))
    } catch (error) {
        console.error('Template download error:', error)
        toast.error(__(error.message || 'Failed to download template'))
    } finally {
        isDownloading.value = false
    }
}

// File handling
const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file && isValidFileType(file)) {
        selectedFile.value = file
        processFilePreview(file)
    } else {
        showFileTypeError()
    }
    event.target.value = ''
}

const handleDrop = (event) => {
    event.preventDefault()
    isDragOver.value = false

    const files = event.dataTransfer.files
    if (files.length > 0) {
        const file = files[0]
        if (isValidFileType(file)) {
            selectedFile.value = file
            processFilePreview(file)
        } else {
            showFileTypeError()
        }
    }
}

const isValidFileType = (file) => {
    const validTypes = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
        'text/csv'
    ]
    const validExtensions = ['.xlsx', '.xls', '.csv']

    return validTypes.includes(file.type) ||
        validExtensions.some(ext => file.name.toLowerCase().endsWith(ext))
}

const showFileTypeError = () => {
    toast.error(__('Please select an Excel (.xlsx, .xls) or CSV file.'))
}

// Các methods khác sẽ được thêm vào file thứ 2...
// JAVASCRIPT METHODS CONTINUATION FROM FILE 1

// File preview processing
const processFilePreview = async (file) => {
    currentStep.value = 'processing'

    try {
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch('/api/method/mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.upload_and_preview_talent', {
            method: 'POST',
            headers: {
                'X-Frappe-CSRF-Token': window.csrf_token
            },
            body: formData
        })

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`)
        }

        const result = await response.json()

        if (result.message) {
            previewData.value = result.message
            availableFields.value = result.message.available_fields || []

            // Auto-map fields
            autoMapFields()

            currentStep.value = 'mapping'
            toast.success(__(`Successfully loaded ${result.message.total_rows} records`))
        } else {
            throw new Error(result.exc || __('Failed to process file'))
        }

    } catch (error) {
        console.error('File preview error:', error)
        toast.error(__(error.message))
        currentStep.value = 'upload'
    }
}

// Field mapping
const autoMapFields = () => {
    if (!previewData.value?.columns || !availableFields.value.length) return

    const mapping = {}
    const columns = previewData.value.columns.map(col => col.toLowerCase())

    const commonMappings = {
    'full_name': ['full_name', 'name', 'full name', 'họ và tên', 'tên đầy đủ', 'hoten', 'ho ten', 'ho_ten'],
    'gender': ['gender', 'giới tính', 'gioi_tinh', 'phai', 'giới tính'],
    'email': ['email', 'primary_email', 'contact_email', 'email address', 'địa chỉ email', 'email_ca_nhan', 'email ca nhan', 'email chinh'],
    'phone': ['phone', 'phone_number', 'contact_phone', 'phone number', 'số điện thoại', 'sdt', 'dien_thoai', 'dien thoai'],
    'linkedin_profile': ['linkedin', 'linkedin_profile', 'linkedin_url', 'linkedin profile', 'lien_ket_linkedin', 'liên kết linkedin', 'link linkedin'],
    'facebook_profile': ['facebook', 'facebook_profile', 'facebook profile', 'lien_ket_facebook', 'liên kết facebook'],
    'zalo_profile': ['zalo', 'zalo_profile', 'zalo profile', 'lien_ket_zalo', 'liên kết zalo'],
    'date_of_birth': ['date_of_birth', 'birth_date', 'dob', 'ngày sinh', 'ngay sinh', 'sinh_nhat'],
    'current_city': ['current_city', 'city', 'address', 'địa chỉ', 'dia chi', 'thành phố', 'thanh pho'],
    'desired_role': ['desired_role', 'desired position', 'vị trí mong muốn', 'vi tri mong muon', 'vai trò mong muốn'],
    'domain_expertise': ['domain_expertise', 'domain expertise', 'chuyên môn lĩnh vực', 'chuyen mon linh vuc', 'industry_knowledge', 'kinh nghiem linh vuc', 'linh vuc chuyen mon'],
    'hard_skills': ['hard_skills', 'hard skills', 'kỹ năng cứng', 'ky nang cung', 'technical_skills', 'ky nang ky thuat', 'technical skill', 'hard skill'],
    'soft_skills': ['soft_skills', 'soft skills', 'kỹ năng mềm', 'ky nang mem', 'interpersonal_skills', 'ky nang giao tiep', 'soft skill'],
    'total_years_of_experience': ['total_years_of_experience', 'years_of_experience', 'experience_years', 'tổng số năm kinh nghiệm', 'tong so nam kinh nghiem', 'kinh nghiem'],
    'latest_company': ['latest_company', 'current_company', 'last_company', 'công ty gần nhất', 'cong ty gan nhat', 'cong ty hien tai'],
    'highest_education': ['highest_education', 'education', 'học vấn cao nhất', 'hoc van cao nhat', 'trinh do hoc van'],
    'current_salary': ['current_salary', 'salary', 'mức lương hiện tại', 'muc luong hien tai', 'luong hien tai'],
    'expected_salary': ['expected_salary', 'expected salary', 'mức lương mong muốn', 'muc luong mong muon', 'salary_expectation', 'luong_mong_muon'],
    'preferred_work_model': ['preferred_work_model', 'work_model', 'hình thức làm việc', 'hinh thuc lam viec', 'mo hinh lam viec'],
    'availability_date': ['availability_date', 'availability date', 'ngày có thể làm việc', 'ngay co the lam viec', 'available_date', 'start_date', 'thoi gian bat dau'],
    'source': ['source', 'nguon', 'nguồn', 'nguon_goc', 'nguồn gốc', 'nguon talent'],
    'recruiter_owner_id': ['recruiter_owner_id', 'recruiter', 'owner', 'người phụ trách', 'nguoi phu trach'],
    'crm_status': ['crm_status', 'pool_status', 'trạng thái pool', 'trang thai pool', 'trang thai crm'],
    'recruitment_readiness': ['recruitment_readiness', 'recruitment readiness', 'sẵn sàng tuyển dụng', 'san sang tuyen dung', 'readiness', 'tinh_trang_tuyen_dung', 'muc do san sang'],
    'last_interaction_date': ['last_interaction_date', 'interaction_date', 'lần tương tác cuối', 'lan tuong tac cuoi', 'ngay tuong tac'],
    'internal_rating': ['internal_rating', 'internal rating', 'đánh giá nội bộ', 'danh gia noi bo', 'rating', 'xep_hang'],
    'priority_level': ['priority_level', 'priority', 'mức độ ưu tiên', 'muc do uu tien', 'do uu tien'],
    'interaction_notes': ['interaction_notes', 'notes', 'ghi chú tương tác', 'ghi chu tuong tac', 'ghi chu'],
    'tags': ['tags', 'labels', 'thẻ/nhãn', 'the nhan', 'nhan'],
    'cultural_fit': ['cultural_fit', 'cultural fit', 'phù hợp văn hóa', 'phu hop van hoa', 'culture_fit', 'van_hoa_cong_ty'],
    'skills': ['skills', 'kỹ năng', 'ky nang', 'ky_nang', 'skill', 'kỹ năng chuyên môn'],
};

    // Define priority order for skill-related fields (specific before general)
    const fieldPriority = {
        'hard_skills': 1,
        'soft_skills': 2, 
        'skills': 3, // General skills has lowest priority
        'domain_expertise': 4
    }
    
    // Sort fields by priority (specific skills first, then general)
    const sortedFields = availableFields.value.sort((a, b) => {
        const priorityA = fieldPriority[a.fieldname] || 999
        const priorityB = fieldPriority[b.fieldname] || 999
        return priorityA - priorityB
    })

    // First pass: Exact matches (highest priority)
    sortedFields.forEach(field => {
        const variations = commonMappings[field.fieldname] || []
        
        for (const header of previewData.value.columns) {
            const normalizedHeader = header.toLowerCase().trim().replace(/[_\s-]/g, '')
            
            for (const variation of variations) {
                const normalizedVariation = variation.toLowerCase().replace(/[_\s-]/g, '')
                if (normalizedHeader === normalizedVariation) {
                    mapping[field.fieldname] = header
                    break
                }
            }
            if (mapping[field.fieldname]) break
        }
    })

    // Second pass: Partial matches for unmapped fields
    sortedFields.forEach(field => {
        if (mapping[field.fieldname]) return // Skip already mapped fields
        
        const variations = commonMappings[field.fieldname] || []
        
        for (const header of previewData.value.columns) {
            // Skip headers already used in mapping
            if (Object.values(mapping).includes(header)) continue
            
            const normalizedHeader = header.toLowerCase().trim().replace(/[_\s-]/g, '')
            
            for (const variation of variations) {
                const normalizedVariation = variation.toLowerCase().replace(/[_\s-]/g, '')
                if (normalizedHeader.includes(normalizedVariation) ||
                    normalizedVariation.includes(normalizedHeader)) {
                    mapping[field.fieldname] = header
                    break
                }
            }
            if (mapping[field.fieldname]) break
        }
    })

    fieldMapping.value = mapping
}

const clearMapping = () => {
    fieldMapping.value = {}
}

// Data validation
const validateData = async () => {
    if (!canProcess.value) return

    isValidating.value = true

    try {
        await processImport(true) // validation only
    } finally {
        isValidating.value = false
    }
}

// Data import
const processImport = async (validationOnly = false) => {
    if (!canProcess.value || !selectedFile.value) return

    isImporting.value = true
    if (!validationOnly) {
        currentStep.value = 'importing'
        startProgressTracking()
    }

    try {
        const formData = new FormData()
        formData.append('file', selectedFile.value)
        formData.append('mapping', JSON.stringify(fieldMapping.value))
        formData.append('validate_only', validationOnly ? '1' : '0')
        
        // Add segment_id if selected
        if (selectedJob.value) {
            formData.append('segment_id', selectedJob.value)
        }

        const response = await fetch('/api/method/mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.import_with_mapping_talent', {
            method: 'POST',
            headers: {
                'X-Frappe-CSRF-Token': window.csrf_token
            },
            body: formData
        })

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`)
        }

        const result = await response.json()

        if (result.message) {
            console.log(result.message)
            importResults.value = result.message
            sessionId.value = result.message.session_id

            if (validationOnly) {
                validateOnly.value = true
            } else {
                validateOnly.value = false
            }

            currentStep.value = 'results'
            stopProgressTracking()

            const actionText = validationOnly ? __('Validation') : __('Import')
            toast.success(__(`Processed ${importResults.value.total} records. ${importResults.value.success} successful, ${importResults.value.failed} failed.`))
            
            // Emit created event if import was successful and not validation only
            if (!validationOnly && importResults.value.success > 0) {
                emit('created', {
                    success: importResults.value.success,
                    failed: importResults.value.failed,
                    total: importResults.value.total
                })
            }
        } else {
            throw new Error(result.exc || __('Import failed'))
        }

    } catch (error) {
        console.error('Import error:', error)
        toast.error(__(error.message))
        currentStep.value = 'mapping'
    } finally {
        isImporting.value = false
        stopProgressTracking()
    }
}

const proceedWithImport = () => {
    validateOnly.value = false
    processImport(false)
}

// Progress tracking
const startProgressTracking = () => {
    if (!sessionId.value) return

    progressInterval = setInterval(async () => {
        try {
            const progress = await call('mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.get_import_progress', {
                session_id: sessionId.value
            })

            if (progress) {
                importProgress.value = progress

                if (progress.status === 'Completed') {
                    stopProgressTracking()
                }
            }
        } catch (error) {
            console.error('Progress tracking error:', error)
        }
    }, 1000)
}

const stopProgressTracking = () => {
    if (progressInterval) {
        clearInterval(progressInterval)
        progressInterval = null
    }
}

const handleProgressUpdate = (data) => {
    if (data.session_id === sessionId.value) {
        importProgress.value = {
            processed: data.processed,
            total: data.total,
            success: data.success,
            failed: data.failed
        }
    }
}

// Utility methods
const resetUpload = () => {
    currentStep.value = 'upload'
    selectedFile.value = null
    previewData.value = null
    availableFields.value = []
    fieldMapping.value = {}
    importResults.value = null
    importProgress.value = null
    sessionId.value = null
    validateOnly.value = false
    isDragOver.value = false
    logFilter.value = 'all'
    stopProgressTracking()
}

const goBackToUpload = () => {
    currentStep.value = 'upload'
    selectedFile.value = null
    previewData.value = null
    fieldMapping.value = {}
}

const closeModal = () => {
    show.value = false
    emit('close')
}

const downloadErrorLog = () => {
    if (!importResults.value?.logs) return

    const errorLogs = importResults.value.logs.filter(log => log.status === 'error')
    if (errorLogs.length === 0) return

    const csvContent = [
        ['Row Number', 'Candidate Name', 'Error Message'],
        ...errorLogs.map(log => [
            log.row_number || '',
            log.candidate_name || '',
            (log.message || '').replace(/"/g, '""')
        ])
    ].map(row => row.map(cell => `"${cell}"`).join(',')).join('\n')

    const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `can_import_errors_${new Date().toISOString().split('T')[0]}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
}

const goToTalentList = () => {
    closeModal()
}

// Style helper methods
const getLogEntryClass = (status) => {
    switch (status) {
        case 'success':
            return 'success'
        case 'error':
            return 'error'
        case 'warning':
            return 'warning'
        default:
            return 'default'
    }
}

const getStatusBadgeClass = (status) => {
    switch (status) {
        case 'success':
            return 'bg-green-100 text-green-800'
        case 'error':
            return 'bg-red-100 text-red-800'
        case 'warning':
            return 'bg-yellow-100 text-yellow-800'
        default:
            return 'bg-gray-100 text-gray-800'
    }
}

// Import history methods
const getSessionStatusClass = (status) => {
    switch (status) {
        case 'Completed':
            return 'bg-green-100 text-green-800'
        case 'Failed':
            return 'bg-red-100 text-red-800'
        case 'Processing':
            return 'bg-blue-100 text-blue-800'
        default:
            return 'bg-gray-100 text-gray-800'
    }
}

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString()
}

const refreshImportHistory = async () => {
    loadingHistory.value = true
    try {
        const history = await call('mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.get_import_history')
        importHistory.value = history || []
    } catch (error) {
        console.error('Error loading import history:', error)
        toast.error(__('Failed to load import history'))
    } finally {
        loadingHistory.value = false
    }
}

const retrySession = async (sessionName) => {
    if (retryingSessions.value.includes(sessionName)) return

    retryingSessions.value.push(sessionName)

    try {
        const result = await call('mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.retry_failed_import', {
            session_id: sessionName
        })

        if (result) {
            toast.success(__(result.message || 'Import retry has been initiated'))

            // Refresh history after short delay
            setTimeout(() => {
                refreshImportHistory()
            }, 2000)
        }
    } catch (error) {
        console.error('Retry session error:', error)
        toast.error(__(error.message || 'Failed to retry import session'))
    } finally {
        retryingSessions.value = retryingSessions.value.filter(id => id !== sessionName)
    }
}

const viewSessionDetails = async (sessionName) => {
    try {
        const details = await call('mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.get_session_details', {
            session_id: sessionName
        })

        if (details) {
            selectedSessionDetails.value = details
            showSessionDetails.value = true
        }
    } catch (error) {
        console.error('Error loading session details:', error)
        toast.error(__('Failed to load session details'))
    }
}

// delete session (dont)
const deleteSession = async (sessionName) => {
    if (!confirm(__('Are you sure you want to delete this import session?'))) {
        return
    }

    try {
        await call('mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.delete_import_session', {
            session_id: sessionName
        })

        toast.success(__('Import session has been deleted successfully'))

        // Refresh history
        refreshImportHistory()

    } catch (error) {
        console.error('Delete session error:', error)
        toast.error(__(error.message || __('Failed to delete import session')))
    }
}

// Cancel and retry functionality
const cancelImport = async () => {
    if (!sessionId.value) return

    try {
        await call('mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.cancel_import_session', {
            session_id: sessionId.value
        })
        toast.success(__('Import has been cancelled successfully.'))

        currentStep.value = 'results'
        stopProgressTracking()

    } catch (error) {
        console.error('Cancel import error:', error)
        toast.error(__(error.message || 'Failed to cancel import'))
    }
}

const retryFailedImport = async () => {
    if (!sessionId.value) return

    const isRetrying = ref(false)
    isRetrying.value = true

    try {
        const result = await call('mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.retry_failed_import', {
            session_id: sessionId.value
        })

        if (result) {
            toast.success(__(result.message))

            if (result.retry_session_id) {
                sessionId.value = result.retry_session_id
                startProgressTracking()
                currentStep.value = 'importing'
            }
        }

    } catch (error) {
        console.error('Retry import error:', error)
        toast.error(__(error.message || __('Failed to retry import')))
    } finally {
        isRetrying.value = false
    }
}

const exportFailedRows = async () => {
    if (!sessionId.value) return

    try {
        const result = await call('mbw_mira.mbw_mira.doctype.mira_importsession.mira_importsession.export_failed_rows', {
            session_id: sessionId.value
        })

        if (result?.file_url) {
            const link = document.createElement('a')
            link.href = result.file_url
            link.download = result.file_name
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)

            toast.success(__(`Failed rows exported: ${result.failed_count} records`))
        }

    } catch (error) {
        console.error('Export failed rows error:', error)
        toast.error(__(error.message || __('Failed to export failed rows')))
    }
}
</script>

<style scoped>
/* Main Layout */
.candidate-uploader {
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
}

/* Step Content */
.step-content {
    animation: slideIn 0.3s ease-in-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.step-header {
    text-align: center;
    margin-bottom: 32px;
    padding-bottom: 16px;
    border-bottom: 1px solid #e5e7eb;
}

.step-title {
    font-size: 24px;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 8px;
}

.step-description {
    font-size: 16px;
    color: #6b7280;
}

/* Card Components */
.card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: all 0.2s ease;
}

.card:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.card-header {
    padding: 20px 24px 16px;
    border-bottom: 1px solid #f3f4f6;
    background: #fafafa;
}

.card-title {
    font-size: 16px;
    font-weight: 600;
    color: #1f2937;
    margin: 0;
}

.card-subtitle {
    font-size: 14px;
    color: #6b7280;
    margin: 4px 0 0 0;
}

.card-body {
    padding: 24px;
}

/* Icon Circles */
.icon-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

/* Drop Zone */
.drop-zone {
    border: 2px dashed #d1d5db;
    border-radius: 12px;
    transition: all 0.3s ease;
    background-color: #fafafa;
    cursor: pointer;
}

.drop-zone:hover,
.drop-zone.drag-over {
    border-color: #3b82f6;
    background-color: #eff6ff;
    transform: scale(1.01);
}

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid transparent;
    font-size: 14px;
    text-decoration: none;
    line-height: 1.4;
}

.btn-sm {
    padding: 6px 12px;
    font-size: 12px;
}

.btn-lg {
    padding: 14px 28px;
    font-size: 16px;
}

.btn-primary {
    background-color: gray;
    color: white;
    border-color: gray;
}

.btn-primary:hover:not(:disabled) {
    background-color: gray;
    border-color: gray;
    transform: translateY(-1px);
}

.btn-success {
    background-color: #10b981;
    color: white;
    border-color: #10b981;
}

.btn-success:hover:not(:disabled) {
    background-color: #059669;
    border-color: #059669;
}

.btn-outline {
    border-color: #d1d5db;
    color: #374151;
    background-color: white;
}

.btn-outline:hover:not(:disabled) {
    background-color: #f9fafb;
    border-color: #9ca3af;
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

/* Field Mapping Grid */
.mapping-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
}

@media (min-width: 768px) {
    .mapping-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Field Mapping */
.mapping-field {
    padding: 16px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    background: #fafafa;
    transition: all 0.2s ease;
}

.mapping-field:hover {
    background: #f3f4f6;
    border-color: #d1d5db;
}

.mapping-field select {
    appearance: none;
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
    background-position: right 8px center;
    background-repeat: no-repeat;
    background-size: 16px 12px;
    padding-right: 40px;
    transition: all 0.2s ease;
}

.mapping-field select:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Progress & Loading */
.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f4f6;
    border-top: 4px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto;
}

.progress-spinner {
    width: 60px;
    height: 60px;
    border: 6px solid #f3f4f6;
    border-top: 6px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

/* Statistics Cards */
.stat-card {
    padding: 24px;
    border-radius: 12px;
    text-align: center;
    border: 2px solid;
    transition: all 0.2s ease;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.1);
}

.stat-card.success {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    border-color: #10b981;
}

.stat-card.error {
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    border-color: #ef4444;
}

.stat-card.total {
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    border-color: #3b82f6;
}

.stat-value {
    font-size: 32px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 8px;
}

.stat-card.success .stat-value {
    color: #047857;
}

.stat-card.error .stat-value {
    color: #dc2626;
}

.stat-card.total .stat-value {
    color: #1d4ed8;
}

.stat-label {
    font-size: 14px;
    font-weight: 500;
    opacity: 0.8;
}

/* Log Entries */
.log-entry {
    padding: 16px;
    border-radius: 8px;
    border-left: 4px solid;
    margin-bottom: 8px;
    transition: all 0.2s ease;
}

.log-entry:hover {
    transform: translateX(4px);
}

.log-entry.success {
    background: #f0fdf4;
    border-left-color: #22c55e;
}

.log-entry.error {
    background: #fef2f2;
    border-left-color: #ef4444;
}

.log-entry.warning {
    background: #fffbeb;
    border-left-color: #f59e0b;
}

/* Status Badges */
.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.025em;
}

.bg-green-100 {
    background-color: #dcfce7;
    color: #166534;
}

.bg-red-100 {
    background-color: #fee2e2;
    color: #991b1b;
}

.bg-yellow-100 {
    background-color: #fef3c7;
    color: #92400e;
}

.bg-gray-100 {
    background-color: #f3f4f6;
    color: #374151;
}

.bg-blue-100 {
    background-color: #dbeafe;
    color: #1e40af;
}

/* Alerts */
.alert {
    padding: 16px;
    border-radius: 8px;
    border: 1px solid;
}

.alert-warning {
    background-color: #fffbeb;
    border-color: #fbbf24;
    color: #92400e;
}

/* Form Elements */
.form-checkbox {
    border-radius: 4px;
    border: 2px solid #d1d5db;
    transition: all 0.2s ease;
}

.form-checkbox:checked {
    background-color: #3b82f6;
    border-color: #3b82f6;
}

.form-checkbox:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Transitions and Animations */
.animate-spin {
    animation: spin 1s linear infinite;
}

.transition-all {
    transition: all 0.3s ease;
}

/* Table Styling */
.overflow-x-auto table {
    border-collapse: separate;
    border-spacing: 0;
}

.overflow-x-auto th,
.overflow-x-auto td {
    white-space: nowrap;
}

.max-w-xs {
    max-width: 200px;
}

.truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* Progress Bar */
.bg-blue-600 {
    background-color: #2563eb;
}

.h-3 {
    height: 12px;
}

.rounded-full {
    border-radius: 9999px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .candidate-uploader {
        padding: 16px;
    }

    .step-header {
        margin-bottom: 24px;
    }

    .step-title {
        font-size: 20px;
    }

    .card-header,
    .card-body {
        padding: 16px;
    }

    .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-3 {
        grid-template-columns: 1fr;
        gap: 16px;
    }

    .grid.grid-cols-1.md\\:grid-cols-3 {
        grid-template-columns: 1fr;
        gap: 12px;
    }

    .flex.space-x-3 {
        flex-direction: column;
        gap: 8px;
    }

    .flex.space-x-3>*+* {
        margin-left: 0;
    }

    .btn {
        justify-content: center;
        width: 100%;
    }

    .drop-zone {
        padding: 16px;
    }

    .stat-card {
        padding: 16px;
    }

    .stat-value {
        font-size: 24px;
    }
}

@media (max-width: 480px) {
    .step-title {
        font-size: 18px;
    }

    .step-description {
        font-size: 14px;
    }

    .card-title {
        font-size: 14px;
    }

    .card-subtitle {
        font-size: 12px;
    }
}

/* Dark mode support (if needed) */
@media (prefers-color-scheme: dark) {
    .card {
        background: #1f2937;
        border-color: #374151;
    }

    .card-header {
        background: #111827;
        border-color: #374151;
    }

    .card-title {
        color: #f9fafb;
    }

    .card-subtitle {
        color: #9ca3af;
    }

    .step-title {
        color: #f9fafb;
    }

    .step-description {
        color: #9ca3af;
    }
}

/* Print styles */
@media print {
    .candidate-uploader {
        padding: 0;
    }

    .step-content {
        animation: none;
    }

    .card {
        box-shadow: none;
        border: 1px solid #000;
    }

    .btn {
        display: none;
    }
}

/* Accessibility improvements */
.btn:focus {
    outline: 2px solid #3b82f6;
    outline-offset: 2px;
}

.mapping-field select:focus {
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* High contrast mode support */
@media (prefers-contrast: high) {
    .card {
        border-width: 2px;
    }

    .btn {
        border-width: 2px;
    }

    .drop-zone {
        border-width: 3px;
    }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
    .step-content {
        animation: none;
    }

    .spinner,
    .progress-spinner {
        animation: none;
    }

    .btn,
    .card,
    .log-entry {
        transition: none;
    }

    .drop-zone {
        transform: none;
    }

    .card:hover,
    .btn:hover,
    .log-entry:hover {
        transform: none;
    }
}

/* Additional utility classes */
.text-green-600 {
    color: #059669;
}

.text-red-600 {
    color: #dc2626;
}

.text-blue-600 {
    color: #2563eb;
}

.text-yellow-600 {
    color: #d97706;
}

.text-gray-600 {
    color: #4b5563;
}

.text-gray-500 {
    color: #6b7280;
}

.text-gray-400 {
    color: #9ca3af;
}

.bg-gray-50 {
    background-color: #f9fafb;
}

.bg-gray-200 {
    background-color: #e5e7eb;
}

.border-gray-300 {
    border-color: #d1d5db;
}

.border-red-500 {
    border-color: #ef4444;
}

.ring-red-500 {
    --tw-ring-color: #ef4444;
}

.ring-blue-500 {
    --tw-ring-color: #3b82f6;
}

/* Focus ring utilities */
.focus\:ring-2:focus {
    --tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);
    --tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color);
    box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000);
}

.focus\:border-blue-500:focus {
    border-color: #3b82f6;
}

/* Grid utilities */
.grid {
    display: grid;
}

.grid-cols-1 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
}

.gap-4 {
    gap: 1rem;
}

.gap-8 {
    gap: 2rem;
}

.gap-12 {
    gap: 3rem;
}

.gap-16 {
    gap: 4rem;
}

/* Flex utilities */
.flex {
    display: flex;
}

.flex-1 {
    flex: 1 1 0%;
}

.flex-shrink-0 {
    flex-shrink: 0;
}

.items-center {
    align-items: center;
}

.items-start {
    align-items: flex-start;
}

.justify-center {
    justify-content: center;
}

.justify-between {
    justify-content: space-between;
}

.space-x-2>*+* {
    margin-left: 0.5rem;
}

.space-x-3>*+* {
    margin-left: 0.75rem;
}

.space-x-4>*+* {
    margin-left: 1rem;
}

.space-y-2>*+* {
    margin-top: 0.5rem;
}

.space-y-3>*+* {
    margin-top: 0.75rem;
}

.space-y-4>*+* {
    margin-top: 1rem;
}

/* Spacing utilities */
.p-4 {
    padding: 1rem;
}

.p-5 {
    padding: 1.25rem;
}

.p-6 {
    padding: 1.5rem;
}

.p-8 {
    padding: 2rem;
}

.px-3 {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
}

.px-4 {
    padding-left: 1rem;
    padding-right: 1rem;
}

.py-1 {
    padding-top: 0.25rem;
    padding-bottom: 0.25rem;
}

.py-2 {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
}

.py-4 {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.py-8 {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.py-12 {
    padding-top: 3rem;
    padding-bottom: 3rem;
}

.mb-1 {
    margin-bottom: 0.25rem;
}

.mb-2 {
    margin-bottom: 0.5rem;
}

.mb-3 {
    margin-bottom: 0.75rem;
}

.mb-4 {
    margin-bottom: 1rem;
}

.mb-6 {
    margin-bottom: 1.5rem;
}

.mb-8 {
    margin-bottom: 2rem;
}

.mr-1 {
    margin-right: 0.25rem;
}

.mr-2 {
    margin-right: 0.5rem;
}

.mr-3 {
    margin-right: 0.75rem;
}

.ml-2 {
    margin-left: 0.5rem;
}

.ml-3 {
    margin-left: 0.75rem;
}

.mt-1 {
    margin-top: 0.25rem;
}

.mt-2 {
    margin-top: 0.5rem;
}

.mt-6 {
    margin-top: 1.5rem;
}

/* Width and height utilities */
.w-4 {
    width: 1rem;
}

.w-5 {
    width: 1.25rem;
}

.w-8 {
    width: 2rem;
}

.w-12 {
    width: 3rem;
}

.w-16 {
    width: 4rem;
}

.w-full {
    width: 100%;
}

.h-0\.5 {
    height: 0.125rem;
}

.h-4 {
    height: 1rem;
}

.h-5 {
    height: 1.25rem;
}

.h-8 {
    height: 2rem;
}

.h-12 {
    height: 3rem;
}

.h-16 {
    height: 4rem;
}

.max-h-64 {
    max-height: 16rem;
}

.max-h-96 {
    max-height: 24rem;
}

.max-w-md {
    max-width: 28rem;
}

/* Position utilities */
.sticky {
    position: sticky;
}

.top-0 {
    top: 0;
}

/* Text utilities */
.text-xs {
    font-size: 0.75rem;
    line-height: 1rem;
}

.text-sm {
    font-size: 0.875rem;
    line-height: 1.25rem;
}

.text-lg {
    font-size: 1.125rem;
    line-height: 1.75rem;
}

.text-xl {
    font-size: 1.25rem;
    line-height: 1.75rem;
}

.text-2xl {
    font-size: 1.5rem;
    line-height: 2rem;
}

.font-medium {
    font-weight: 500;
}

.font-semibold {
    font-weight: 600;
}

.font-bold {
    font-weight: 700;
}

.uppercase {
    text-transform: uppercase;
}

.text-center {
    text-align: center;
}

.text-left {
    text-align: left;
}

/* Border utilities */
.border {
    border-width: 1px;
}

.border-b {
    border-bottom-width: 1px;
}

.border-l {
    border-left-width: 1px;
}

.border-2 {
    border-width: 2px;
}

.rounded {
    border-radius: 0.25rem;
}

.rounded-md {
    border-radius: 0.375rem;
}

.rounded-lg {
    border-radius: 0.5rem;
}

.rounded-full {
    border-radius: 9999px;
}

/* Display utilities */
.block {
    display: block;
}

.inline-block {
    display: inline-block;
}

.hidden {
    display: none;
}

/* Overflow utilities */
.overflow-hidden {
    overflow: hidden;
}

.overflow-x-auto {
    overflow-x: auto;
}

.overflow-y-auto {
    overflow-y: auto;
}

/* Cursor utilities */
.cursor-pointer {
    cursor: pointer;
}

.cursor-not-allowed {
    cursor: not-allowed;
}

/* Opacity utilities */
.opacity-50 {
    opacity: 0.5;
}

.opacity-80 {
    opacity: 0.8;
}

/* Transform utilities */
.transform {
    transform: var(--tw-transform);
}

.scale-101 {
    --tw-scale-x: 1.01;
    --tw-scale-y: 1.01;
    transform: scale(var(--tw-scale-x), var(--tw-scale-y));
}

/* Transition utilities */
.duration-300 {
    transition-duration: 300ms;
}

.duration-500 {
    transition-duration: 500ms;
}

.ease-in-out {
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>