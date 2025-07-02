<template>
  <v-app>
    <v-main class="login-background">
      <div class="login-center">
        <v-card
          class="login-card"
          elevation="0"
        >
          <!-- Logo -->
          <v-img
            src="https://mbw.vn/wp-content/uploads/2023/09/logo-1.png"
            max-width="80"
            class="mx-auto mb-4"
            alt="Logo"
          />

          <!-- Titles -->
          <v-card-title class="text-h5 text-center font-weight-bold mb-1">
            Welcome Back
          </v-card-title>
          <v-card-subtitle class="text-center mb-5 text-grey-darken-1">
            Sign in to your account
          </v-card-subtitle>

          <!-- Form -->
          <v-form @submit.prevent="handleLogin">
            <v-text-field
              v-model="email"
              label="Email or Username"
              prepend-inner-icon="mdi-account"
              variant="outlined"
              autocomplete="username"
              required
              density="comfortable"
              class="mb-4"
              :style="fieldStyle"
            />

            <v-text-field
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              label="Password"
              prepend-inner-icon="mdi-lock"
              :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showPassword = !showPassword"
              variant="outlined"
              autocomplete="current-password"
              required
              density="comfortable"
              class="mb-4"
              :style="fieldStyle"
            />

            <v-alert
              v-if="error"
              type="error"
              variant="tonal"
              class="mb-4"
              density="compact"
            >
              {{ error }}
            </v-alert>

            <v-btn
              :loading="loading"
              type="submit"
              color="#6366f1"
              variant="flat"
              size="large"
              block
              rounded
            >
              Login
            </v-btn>
          </v-form>
        </v-card>
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { sessionStore as session } from '@/stores/session'

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const error = ref('')
const loading = ref(false)

// Vuetify CSS variables override
const fieldStyle = {
  '--v-field-border-color': '#bbb',
  '--v-field-focused-border-color': '#888',
  '--v-input-label-color': '#888',
  '--v-field-active-label-color': '#888'
}

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await session().login.submit({ email: email.value, password: password.value })
  } catch (e) {
    error.value = e.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-background {
  height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #f3f4f6 0%, #e8eaef 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px;
  box-sizing: border-box;
  overflow: hidden;
}

.login-center {
  width: 100%;
  max-width: 420px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
}

.login-card {
  width: 100%;
  border-radius: 20px;
  background-color: #ffffff;
  padding: 32px 24px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  border: 1px solid #e0e0e0;
  transition: box-shadow 0.3s ease;
}

.login-card:hover {
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
}
</style>
