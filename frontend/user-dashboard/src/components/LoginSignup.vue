<template>
  <div v-if="isOpen" class="auth-modal-overlay common-scroolbar" @click.self="closeModal">
    <div
      class="auth-modal-container common-scroolbar"
      :class="{ 'dark-mode': isDarkMode }"
    >
      <!-- Close Button -->
      <button class="auth-close-btn" @click="closeModal">
        <i class="fas fa-times"></i>
      </button>

      <!-- Logo Header -->
      <div class="auth-logo-header">
        <i class="fas fa-music"></i>
        <h1>Injustify</h1>
        <i class="fas fa-music"></i>
      </div>

      <!-- Login Form -->
      <div v-if="activeForm === 'login'" class="auth-form">
        <h2>Welcome Back</h2>
        <p class="auth-subtitle">Login to access your music library</p>

        <form @submit.prevent="login" class="auth-form-content">
          <div class="form-group">
            <label for="login-email">Email</label>
            <div class="input-with-icon">
              <i class="fas fa-envelope"></i>
              <input
                id="login-email"
                v-model="loginData.email"
                type="email"
                placeholder="Enter your email"
                required
                class="auth-input"
                :class="{ error: loginErrors.email }"
                @input="clearError('login', 'email')"
              />
            </div>
            <span v-if="loginErrors.email" class="error-message">{{
              loginErrors.email
            }}</span>
          </div>

          <div class="form-group">
            <label for="login-password">Password</label>
            <div class="input-with-icon password-input">
              <i class="fas fa-lock"></i>
              <input
                id="login-password"
                v-model="loginData.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Enter your password"
                required
                class="auth-input"
                :class="{ error: loginErrors.password }"
                @input="clearError('login', 'password')"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
                tabindex="-1"
              >
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
            <span v-if="loginErrors.password" class="error-message">{{
              loginErrors.password
            }}</span>
          </div>

          <div class="form-options">
            <label class="checkbox-container">
              <input type="checkbox" v-model="loginData.rememberMe" />
              <span class="checkmark"></span>
              Remember me
            </label>
            <a href="#" @click.prevent="switchForm('reset')" class="auth-link"
              >Forgot password?</a
            >
          </div>

          <button type="submit" class="auth-btn primary" :disabled="isLoading">
            <span v-if="!isLoading">Login</span>
            <div v-else class="auth-spinner"></div>
          </button>

          <div class="auth-divider">
            <span>or continue with</span>
          </div>

          <button
            type="button"
            class="auth-btn google-btn"
            @click="authWithGoogle"
            :disabled="isLoading"
          >
            <img src="../assets/google_logo.png" alt="Google Logo" />
            <span>Google</span>
          </button>

          <p class="auth-switch-text">
            Don't have an account?
            <a href="#" @click.prevent="switchForm('signup')" class="auth-link"
              >Sign up</a
            >
          </p>
        </form>
      </div>

      <!-- Signup Form -->
      <div v-if="activeForm === 'signup'" class="auth-form">
        <h2>Create Account</h2>
        <p class="auth-subtitle">Join to discover new music</p>

        <form @submit.prevent="signup" class="auth-form-content">
          <div class="form-group">
            <label for="signup-email">Email</label>
            <div class="input-with-icon">
              <i class="fas fa-envelope"></i>
              <input
                id="signup-email"
                v-model="signupData.email"
                type="email"
                placeholder="Enter your email"
                required
                class="auth-input"
                :class="{ error: signupErrors.email }"
                @input="clearError('signup', 'email')"
              />
            </div>
            <span v-if="signupErrors.email" class="error-message">{{
              signupErrors.email
            }}</span>
          </div>

          <div class="form-group">
            <label for="signup-username">Username</label>
            <div class="input-with-icon">
              <i class="fas fa-user"></i>
              <input
                id="signup-username"
                v-model="signupData.username"
                type="text"
                placeholder="Choose a username"
                required
                class="auth-input"
                :class="{ error: signupErrors.username }"
                @input="clearError('signup', 'username')"
              />
            </div>
            <span v-if="signupErrors.username" class="error-message">{{
              signupErrors.username
            }}</span>
          </div>

          <div class="form-group">
            <label for="signup-password">Password</label>
            <div class="input-with-icon password-input">
              <i class="fas fa-lock"></i>
              <input
                id="signup-password"
                v-model="signupData.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Create a password"
                required
                class="auth-input"
                :class="{ error: signupErrors.password }"
                @input="
                  validatePassword();
                  clearError('signup', 'password');
                "
              />
              <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
                tabindex="-1"
              >
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
            <div class="password-strength" v-if="signupData.password">
              <div class="strength-meter">
                <div class="strength-bar" :class="passwordStrengthClass"></div>
              </div>
              <span class="strength-text">{{ passwordStrengthText }}</span>
            </div>
            <ul class="password-requirements">
              <li :class="{ met: hasMinLength }">
                <i :class="hasMinLength ? 'fas fa-check-circle' : 'far fa-circle'"></i>
                At least 8 characters
              </li>
              <li :class="{ met: hasUpperCase }">
                <i :class="hasUpperCase ? 'fas fa-check-circle' : 'far fa-circle'"></i>
                At least 1 uppercase letter
              </li>
              <li :class="{ met: hasNumber }">
                <i :class="hasNumber ? 'fas fa-check-circle' : 'far fa-circle'"></i>
                At least 1 number
              </li>
              <li :class="{ met: hasSpecialChar }">
                <i :class="hasSpecialChar ? 'fas fa-check-circle' : 'far fa-circle'"></i>
                At least 1 special character (!@#$%^&*)
              </li>
            </ul>
            <span v-if="signupErrors.password" class="error-message">{{
              signupErrors.password
            }}</span>
          </div>

          <div class="form-group">
            <label for="signup-confirm-password">Confirm Password</label>
            <div class="input-with-icon password-input">
              <i class="fas fa-lock"></i>
              <input
                id="signup-confirm-password"
                v-model="signupData.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                placeholder="Confirm your password"
                required
                class="auth-input"
                :class="{ error: signupErrors.confirmPassword }"
                @input="clearError('signup', 'confirmPassword')"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showConfirmPassword = !showConfirmPassword"
                tabindex="-1"
              >
                <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
            <span v-if="signupErrors.confirmPassword" class="error-message">{{
              signupErrors.confirmPassword
            }}</span>
          </div>

          <div class="form-group terms-group">
            <label class="checkbox-container">
              <input
                type="checkbox"
                v-model="signupData.termsAccepted"
                required
                :class="{ error: signupErrors.termsAccepted }"
              />
              <span
                class="checkmark"
                :class="{ error: signupErrors.termsAccepted }"
              ></span>
              I agree to the
              <a href="/terms" target="_blank" class="auth-link">Terms and Conditions</a>
            </label>
            <span v-if="signupErrors.termsAccepted" class="error-message">{{
              signupErrors.termsAccepted
            }}</span>
          </div>

          <button
            type="submit"
            class="auth-btn primary"
            :disabled="isLoading || !canSignup"
          >
            <span v-if="!isLoading">Sign Up</span>
            <div v-else class="auth-spinner"></div>
          </button>

          <div class="auth-divider">
            <span>or sign up with</span>
          </div>

          <button
            type="button"
            class="auth-btn google-btn"
            @click="authWithGoogle"
            :disabled="isLoading"
          >
            <img src="../assets/google_logo.png" alt="Google Logo" />
            <span>Google</span>
          </button>

          <p class="auth-switch-text">
            Already have an account?
            <a href="#" @click.prevent="switchForm('login')" class="auth-link">Login</a>
          </p>

          <div v-if="signupSuccess" class="auth-message success">
            <i class="fas fa-check-circle"></i>
            Almost there! Please check your email and click the verification link to
            complete your signup.
          </div>
        </form>
      </div>

      <!-- Reset Password Form -->
      <div v-if="activeForm === 'reset'" class="auth-form">
        <h2>Reset Password</h2>
        <p class="auth-subtitle" v-if="!resetData.approved">
          Enter your email to receive a reset code
        </p>
        <p class="auth-subtitle" v-else>Create your new password</p>

        <div class="auth-form-content">
          <div v-if="!resetData.approved">
            <div class="form-group">
              <label for="reset-email">Email</label>
              <div class="input-with-icon">
                <i class="fas fa-envelope"></i>
                <input
                  id="reset-email"
                  v-model="resetData.email"
                  type="email"
                  placeholder="Enter your email"
                  required
                  class="auth-input"
                  :class="{ error: resetErrors.email }"
                  :disabled="isLoading"
                  @input="clearError('reset', 'email')"
                />
              </div>
              <span v-if="resetErrors.email" class="error-message">{{
                resetErrors.email
              }}</span>
            </div>

            <button
              type="button"
              class="auth-btn primary"
              @click="sendResetCode"
              :disabled="!isValidEmail || isLoading"
            >
              <span v-if="!isLoading">Send Reset Code</span>
              <div v-else class="auth-spinner"></div>
            </button>

            <div v-if="resetMessage" class="auth-message" :class="resetMessage.type">
              <i :class="resetMessage.icon"></i>
              {{ resetMessage.text }}
            </div>

            <div
              class="verification-code"
              v-if="resetData.codeSent && !resetErrors.email"
            >
              <p>Enter the 6-digit code sent to your email:</p>
              <div class="code-inputs">
                <input
                  v-for="(digit, index) in resetData.code"
                  :key="index"
                  v-model="resetData.code[index]"
                  :id="'digit' + (index + 1)"
                  type="text"
                  maxlength="1"
                  pattern="[0-9]"
                  @input="moveNext($event, index)"
                  @keydown="preventInvalidInput($event, index)"
                  class="code-input"
                  :class="{ error: resetErrors.code }"
                  autocomplete="off"
                  :disabled="isLoading"
                />
              </div>
              <span v-if="resetErrors.code" class="error-message">{{
                resetErrors.code
              }}</span>
            </div>
          </div>

          <div v-if="resetData.approved" class="new-password-form">
            <div class="form-group">
              <label for="new-password">New Password</label>
              <div class="input-with-icon password-input">
                <i class="fas fa-lock"></i>
                <input
                  id="new-password"
                  v-model="resetData.newPassword"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Create a new password"
                  required
                  class="auth-input"
                  :class="{ error: resetErrors.newPassword }"
                  @input="
                    validateResetPassword();
                    clearError('reset', 'newPassword');
                  "
                />
                <button
                  type="button"
                  class="password-toggle"
                  @click="showPassword = !showPassword"
                  tabindex="-1"
                >
                  <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
              <span v-if="resetErrors.newPassword" class="error-message">{{
                resetErrors.newPassword
              }}</span>
            </div>

            <div class="form-group">
              <label for="confirm-new-password">Confirm New Password</label>
              <div class="input-with-icon password-input">
                <i class="fas fa-lock"></i>
                <input
                  id="confirm-new-password"
                  v-model="resetData.confirmNewPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  placeholder="Confirm your new password"
                  required
                  class="auth-input"
                  :class="{ error: resetErrors.confirmNewPassword }"
                  @input="clearError('reset', 'confirmNewPassword')"
                />
                <button
                  type="button"
                  class="password-toggle"
                  @click="showConfirmPassword = !showConfirmPassword"
                  tabindex="-1"
                >
                  <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
              <span v-if="resetErrors.confirmNewPassword" class="error-message">{{
                resetErrors.confirmNewPassword
              }}</span>
            </div>

            <button
              type="button"
              class="auth-btn primary"
              @click="resetPassword"
              :disabled="isLoading || !canResetPassword"
            >
              <span v-if="!isLoading && !resetSuccess">Reset Password</span>
              <span v-else-if="resetSuccess">
                <i class="fas fa-check-circle"></i> Successfully
              </span>
              <div v-else class="auth-spinner"></div>
            </button>
          </div>

          <p class="auth-switch-text">
            Remember your password?
            <a href="#" @click.prevent="switchForm('login')" class="auth-link">Login</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "@/store";
import {
  SIGN_UP,
  SEND_EMAIL_RESET_CODES,
  VERIFY_CODES,
  AUTH_WITH_GOOGLE,
  MANUAL_LOGIN,
  RESET_PASSWORD,
} from "@/utils";

export default {
  props: {
    isOpen: Boolean,
    onCloseModal: Function,
    isDarkMode: Boolean,
  },

  data() {
    return {
      activeForm: "login", // 'login', 'signup', 'reset'
      isLoading: false,
      showPassword: false,
      showConfirmPassword: false,
      signupSuccess: false,
      resetSuccess: false,

      // Form data
      loginData: {
        email: "",
        password: "",
        rememberMe: false,
      },

      signupData: {
        email: "",
        username: "",
        password: "",
        confirmPassword: "",
        termsAccepted: false,
      },

      resetData: {
        email: "",
        code: ["", "", "", "", "", ""],
        codeSent: false,
        approved: false,
        newPassword: "",
        confirmNewPassword: "",
      },

      // Error messages
      loginErrors: {
        email: "",
        password: "",
      },

      signupErrors: {
        email: "",
        username: "",
        password: "",
        confirmPassword: "",
        termsAccepted: "",
      },

      resetErrors: {
        email: "",
        code: "",
        newPassword: "",
        confirmNewPassword: "",
      },

      resetMessage: null,

      userStore: useUserStore(),
    };
  },

  computed: {
    // Password strength indicators
    hasMinLength() {
      return (
        this.signupData.password.length >= 8 ||
        (this.activeForm === "reset" && this.resetData.newPassword.length >= 8)
      );
    },

    hasUpperCase() {
      return (
        /[A-Z]/.test(this.signupData.password) ||
        (this.activeForm === "reset" && /[A-Z]/.test(this.resetData.newPassword))
      );
    },

    hasNumber() {
      return (
        /[0-9]/.test(this.signupData.password) ||
        (this.activeForm === "reset" && /[0-9]/.test(this.resetData.newPassword))
      );
    },

    hasSpecialChar() {
      return (
        /[!@#$%^&*]/.test(this.signupData.password) ||
        (this.activeForm === "reset" && /[!@#$%^&*]/.test(this.resetData.newPassword))
      );
    },

    passwordsMatch() {
      if (this.activeForm === "signup") {
        return this.signupData.password === this.signupData.confirmPassword;
      } else if (this.activeForm === "reset") {
        return this.resetData.newPassword === this.resetData.confirmNewPassword;
      }
      return false;
    },

    passwordStrengthClass() {
      if (this.activeForm === "signup" && !this.signupData.password) return "";
      if (this.activeForm === "reset" && !this.resetData.newPassword) return "";

      const password =
        this.activeForm === "signup"
          ? this.signupData.password
          : this.resetData.newPassword;

      const strength =
        (password.length >= 8 ? 1 : 0) +
        (/[A-Z]/.test(password) ? 1 : 0) +
        (/[0-9]/.test(password) ? 1 : 0) +
        (/[!@#$%^&*]/.test(password) ? 1 : 0);

      if (strength <= 1) return "weak";
      if (strength <= 2) return "medium";
      return "strong";
    },

    passwordStrengthText() {
      switch (this.passwordStrengthClass) {
        case "weak":
          return "Weak";
        case "medium":
          return "Medium";
        case "strong":
          return "Strong";
        default:
          return "";
      }
    },

    isValidEmail() {
      const email =
        this.activeForm === "reset"
          ? this.resetData.email
          : this.activeForm === "login"
          ? this.loginData.email
          : this.signupData.email;

      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    },

    canSignup() {
      return (
        this.isValidEmail &&
        this.signupData.username.trim().length > 0 &&
        this.hasMinLength &&
        this.hasUpperCase &&
        this.hasNumber &&
        this.hasSpecialChar &&
        this.passwordsMatch &&
        this.signupData.termsAccepted
      );
    },

    canResetPassword() {
      return (
        this.resetData.newPassword &&
        this.resetData.confirmNewPassword &&
        this.hasMinLength &&
        this.hasUpperCase &&
        this.hasNumber &&
        this.hasSpecialChar &&
        this.passwordsMatch
      );
    },
  },

  methods: {
    // Form switching
    switchForm(form) {
      this.activeForm = form;
      this.clearAllErrors();
      this.resetMessage = null;

      if (form === "signup") {
        this.signupSuccess = false;
      } else if (form === "reset") {
        this.resetSuccess = false;
        this.resetData.codeSent = false;
        this.resetData.approved = false;
        this.resetData.code = ["", "", "", "", "", ""];
      }
    },

    // Error handling
    clearError(form, field) {
      if (form === "login") {
        this.loginErrors[field] = "";
      } else if (form === "signup") {
        this.signupErrors[field] = "";
      } else if (form === "reset") {
        this.resetErrors[field] = "";
      }
    },

    clearAllErrors() {
      this.loginErrors = {
        email: "",
        password: "",
      };

      this.signupErrors = {
        email: "",
        username: "",
        password: "",
        confirmPassword: "",
        termsAccepted: "",
      };

      this.resetErrors = {
        email: "",
        code: "",
        newPassword: "",
        confirmNewPassword: "",
      };
    },

    // Validation
    validatePassword() {
      if (this.activeForm !== "signup") return;

      if (this.signupData.password.length > 32) {
        this.signupErrors.password = "Password must be 32 characters or less";
      }
    },

    validateResetPassword() {
      if (this.activeForm !== "reset") return;

      if (this.resetData.newPassword.length > 32) {
        this.resetErrors.newPassword = "Password must be 32 characters or less";
      }
    },

    // Form submissions
    async login() {
      if (!this.validateLoginForm()) return;

      this.isLoading = true;
      try {
        const response = await axios.post(MANUAL_LOGIN, {
          email: this.loginData.email.trim(),
          password: this.loginData.password,
        });

        this.userStore.set_snackbarMessage("Login successful!", "success", 5000);

        if (response.data.user) {
          this.userStore.setUser(response.data.user);
          this.closeModal();
        }
      } catch (error) {
        this.handleLoginError(error);
      } finally {
        this.isLoading = false;
      }
    },

    validateLoginForm() {
      let isValid = true;

      if (!this.loginData.email.trim()) {
        this.loginErrors.email = "Email is required";
        isValid = false;
      } else if (!this.isValidEmail) {
        this.loginErrors.email = "Please enter a valid email";
        isValid = false;
      }

      if (!this.loginData.password) {
        this.loginErrors.password = "Password is required";
        isValid = false;
      }

      return isValid;
    },

    handleLoginError(error) {
      let errorMessage = "Login failed. Please check your credentials.";

      if (error.response) {
        if (error.response.data.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.response.data.error) {
          errorMessage = error.response.data.error;
        }

        if (error.response.status === 401) {
          this.loginErrors.password = errorMessage;
        } else if (error.response.status === 400 && error.response.data.email) {
          this.loginErrors.email = error.response.data.email[0];
        }
      }

      this.userStore.set_snackbarMessage(errorMessage, "error", 10000);
    },

    async signup() {
      if (!this.validateSignupForm()) return;

      this.isLoading = true;
      try {
        const response = await axios.post(SIGN_UP, {
          email: this.signupData.email.trim(),
          name: this.signupData.username.trim(),
          password: this.signupData.password,
        });

        this.signupSuccess = true;
        this.userStore.set_snackbarMessage(
          "Almost there! Please check your email to complete registration.",
          "success",
          15000
        );

        if (response.data.user) {
          this.userStore.setUser(response.data.user);
          // Clear form but keep email for verification reference
          this.signupData.username = "";
          this.signupData.password = "";
          this.signupData.confirmPassword = "";
          this.signupData.termsAccepted = false;
        }
      } catch (error) {
        this.handleSignupError(error);
      } finally {
        this.isLoading = false;
      }
    },

    validateSignupForm() {
      let isValid = true;

      // Email validation
      if (!this.signupData.email.trim()) {
        this.signupErrors.email = "Email is required";
        isValid = false;
      } else if (!this.isValidEmail) {
        this.signupErrors.email = "Please enter a valid email";
        isValid = false;
      }

      // Username validation
      if (!this.signupData.username.trim()) {
        this.signupErrors.username = "Username is required";
        isValid = false;
      } else if (this.signupData.username.trim().length < 3) {
        this.signupErrors.username = "Username must be at least 3 characters";
        isValid = false;
      }

      // Password validation
      if (!this.signupData.password) {
        this.signupErrors.password = "Password is required";
        isValid = false;
      } else if (this.signupData.password.length < 8) {
        this.signupErrors.password = "Password must be at least 8 characters";
        isValid = false;
      } else if (this.signupData.password.length > 32) {
        this.signupErrors.password = "Password must be 32 characters or less";
        isValid = false;
      } else if (!this.hasUpperCase || !this.hasNumber || !this.hasSpecialChar) {
        this.signupErrors.password = "Password does not meet requirements";
        isValid = false;
      }

      // Confirm password
      if (!this.signupData.confirmPassword) {
        this.signupErrors.confirmPassword = "Please confirm your password";
        isValid = false;
      } else if (!this.passwordsMatch) {
        this.signupErrors.confirmPassword = "Passwords do not match";
        isValid = false;
      }

      // Terms accepted
      if (!this.signupData.termsAccepted) {
        this.signupErrors.termsAccepted = "You must accept the terms and conditions";
        isValid = false;
      }

      return isValid;
    },

    handleSignupError(error) {
      let errorMessage = "Signup failed. Please try again.";

      if (error.response) {
        if (error.response.data.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.response.data.email) {
          this.signupErrors.email = error.response.data.email[0];
          return;
        } else if (error.response.data.username) {
          this.signupErrors.username = error.response.data.username[0];
          return;
        }
      }

      this.userStore.set_snackbarMessage(errorMessage, "error", 10000);
    },

    // Reset password flow
    async sendResetCode() {
      if (!this.resetData.email.trim()) {
        this.resetErrors.email = "Email is required";
        return;
      }

      if (!this.isValidEmail) {
        this.resetErrors.email = "Please enter a valid email";
        return;
      }

      this.isLoading = true;
      try {
        const response = await axios.post(SEND_EMAIL_RESET_CODES, {
          email: this.resetData.email.trim(),
        });

        this.resetData.codeSent = true;
        this.resetMessage = {
          type: "info",
          icon: "fas fa-info-circle",
          text: response.data.message || "Reset code sent to your email",
        };

        this.userStore.set_snackbarMessage(
          "Reset code sent to your email",
          "info",
          10000
        );
      } catch (error) {
        this.handleResetError(error);
      } finally {
        this.isLoading = false;
        this.resetData.codeSent = true;
      }
    },

    async verifyCode() {
      const code = this.resetData.code.join("");

      if (code.length !== 6) {
        this.resetErrors.code = "Please enter the 6-digit code";
        return;
      }

      this.isLoading = true;
      try {
        const response = await axios.post(VERIFY_CODES, {
          email: this.resetData.email.trim(),
          code: code,
        });

        if (response.data.success) {
          this.resetData.approved = true;
          this.resetMessage = {
            type: "success",
            icon: "fas fa-check-circle",
            text: "Code verified! You can now reset your password.",
          };

          this.userStore.set_snackbarMessage(
            "Code verified! You can now reset your password.",
            "success",
            10000
          );
        } else {
          this.resetErrors.code =
            response.data.message || "Invalid code. Please try again.";
          this.shakeCodeInputs();
        }
      } catch (error) {
        this.handleResetError(error);
        this.shakeCodeInputs();
      } finally {
        this.isLoading = false;
      }
    },

    async resetPassword() {
      if (!this.validateResetPasswordForm()) return;

      this.isLoading = true;
      try {
        const response = await axios.post(RESET_PASSWORD, {
          email: this.resetData.email.trim(),
          code: this.resetData.code.join(""),
          password: this.resetData.newPassword,
        });

        this.resetSuccess = true;
        this.resetMessage = {
          type: "success",
          icon: "fas fa-check-circle",
          text: response.data.message || "Password reset successfully!",
        };

        this.userStore.set_snackbarMessage(
          "Password reset successfully!",
          "success",
          5000
        );

        // Auto-close after success
        setTimeout(() => {
          this.switchForm("login");
        }, 2000);
      } catch (error) {
        this.handleResetError(error);
      } finally {
        this.isLoading = false;
      }
    },

    validateResetPasswordForm() {
      let isValid = true;

      if (!this.resetData.newPassword) {
        this.resetErrors.newPassword = "New password is required";
        isValid = false;
      } else if (this.resetData.newPassword.length < 8) {
        this.resetErrors.newPassword = "Password must be at least 8 characters";
        isValid = false;
      } else if (this.resetData.newPassword.length > 32) {
        this.resetErrors.newPassword = "Password must be 32 characters or less";
        isValid = false;
      } else if (!this.hasUpperCase || !this.hasNumber || !this.hasSpecialChar) {
        this.resetErrors.newPassword = "Password does not meet requirements";
        isValid = false;
      }

      if (!this.resetData.confirmNewPassword) {
        this.resetErrors.confirmNewPassword = "Please confirm your new password";
        isValid = false;
      } else if (!this.passwordsMatch) {
        this.resetErrors.confirmNewPassword = "Passwords do not match";
        isValid = false;
      }

      return isValid;
    },

    handleResetError(error) {
      let errorMessage = "An error occurred. Please try again.";

      if (error.response) {
        if (error.response.data.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.response.data.error) {
          errorMessage = error.response.data.error;
        }

        if (error.response.status === 400) {
          if (error.response.data.email) {
            this.resetErrors.email = error.response.data.email[0];
            return;
          } else if (error.response.data.code) {
            this.resetErrors.code = error.response.data.code[0];
            return;
          } else if (error.response.data.password) {
            this.resetErrors.newPassword = error.response.data.password[0];
            return;
          }
        }
      }

      this.resetMessage = {
        type: "error",
        icon: "fas fa-exclamation-circle",
        text: errorMessage,
      };

      this.userStore.set_snackbarMessage(errorMessage, "error", 10000);
    },

    // Code input helpers
    moveNext(event, index) {
      const input = event.target;
      input.value = input.value.replace(/[^0-9]/g, "").slice(0, 1);

      if (input.value && index < 5) {
        document.getElementById(`digit${index + 2}`)?.focus();
      }

      // Auto verify when all digits are entered
      if (this.resetData.code.every((d) => d.length === 1)) {
        this.verifyCode();
      }
    },

    preventInvalidInput(event, index) {
      // Allow navigation with arrow keys
      if (event.key === "ArrowRight" && index < 5) {
        document.getElementById(`digit${index + 2}`)?.focus();
        event.preventDefault();
      } else if (event.key === "ArrowLeft" && index > 0) {
        document.getElementById(`digit${index}`)?.focus();
        event.preventDefault();
      }

      // Prevent non-numeric input
      if (!/[0-9]|Backspace|ArrowLeft|ArrowRight/.test(event.key)) {
        event.preventDefault();
      }

      // Handle backspace
      if (event.key === "Backspace" && !event.target.value && index > 0) {
        document.getElementById(`digit${index}`)?.focus();
      }
    },

    shakeCodeInputs() {
      this.resetErrors.code = "Invalid code. Please try again.";
      const inputs = document.querySelectorAll(".code-input");

      inputs.forEach((input) => {
        input.classList.add("shake");
        setTimeout(() => {
          input.classList.remove("shake");
        }, 500);
      });

      // Clear code and refocus first input
      setTimeout(() => {
        this.resetData.code = ["", "", "", "", "", ""];
        document.getElementById("digit1")?.focus();
      }, 1000);
    },

    // Other methods
    authWithGoogle() {
      window.location.href = AUTH_WITH_GOOGLE;
    },

    closeModal() {
      this.clearAllErrors();
      this.signupSuccess = false;
      this.resetSuccess = false;
      this.resetMessage = null;

      // Reset forms
      this.loginData = {
        email: "",
        password: "",
        rememberMe: false,
      };

      this.signupData = {
        email: "",
        username: "",
        password: "",
        confirmPassword: "",
        termsAccepted: false,
      };

      this.resetData = {
        email: "",
        code: ["", "", "", "", "", ""],
        codeSent: false,
        approved: false,
        newPassword: "",
        confirmNewPassword: "",
      };

      this.$emit("close");
    },
  },
};
</script>

<style scoped>
/* Base Styles */
.auth-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.auth-modal-container {
  position: relative;
  background-color: #ffffff;
  border-radius: 16px;
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.auth-modal-container.dark-mode {
  background-color: #1e1e1e;
  color: #e8eaed;
}

.auth-close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #5f6368;
  cursor: pointer;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s;
}

.auth-close-btn:hover {
  background-color: #f1f3f4;
  color: #202124;
}

.dark-mode .auth-close-btn {
  color: #9aa0a6;
}

.dark-mode .auth-close-btn:hover {
  background-color: #2d2d2d;
  color: #e8eaed;
}

/* Logo Header */
.auth-logo-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.auth-logo-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0;
  color: #4285f4;
}

.auth-logo-header i {
  font-size: 1.5rem;
  color: #4285f4;
}

.dark-mode .auth-logo-header h1,
.dark-mode .auth-logo-header i {
  color: #8ab4f8;
}

/* Auth Form */
.auth-form {
  display: flex;
  flex-direction: column;
}

.auth-form h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 0.5rem;
  text-align: center;
}

.auth-subtitle {
  font-size: 0.875rem;
  color: #5f6368;
  text-align: center;
  margin-bottom: 2rem;
}

.dark-mode .auth-subtitle {
  color: #9aa0a6;
}

.auth-form-content {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Form Groups */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #5f6368;
}

.dark-mode .form-group label {
  color: #9aa0a6;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-icon i {
  position: absolute;
  left: 1rem;
  color: #5f6368;
  font-size: 1rem;
}

.dark-mode .input-with-icon i {
  color: #9aa0a6;
}

.auth-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border-radius: 8px;
  border: 1px solid #dadce0;
  font-size: 0.9375rem;
  transition: all 0.3s;
}

.auth-input:focus {
  outline: none;
  border-color: #4285f4;
  box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2);
}

.dark-mode .auth-input {
  background-color: #2d2d2d;
  border-color: #3c4043;
  color: #e8eaed;
}

.dark-mode .auth-input:focus {
  border-color: #8ab4f8;
  box-shadow: 0 0 0 2px rgba(138, 180, 248, 0.2);
}

/* Password Input */
.password-input {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  color: #5f6368;
  cursor: pointer;
  font-size: 1rem;
}

.dark-mode .password-toggle {
  color: #9aa0a6;
}

/* Password Strength */
.password-strength {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.strength-meter {
  flex: 1;
  height: 4px;
  background-color: #dadce0;
  border-radius: 2px;
  overflow: hidden;
}

.dark-mode .strength-meter {
  background-color: #3c4043;
}

.strength-bar {
  height: 100%;
  width: 0%;
  transition: width 0.3s, background-color 0.3s;
}

.strength-bar.weak {
  width: 25%;
  background-color: #ea4335;
}

.strength-bar.fair {
  width: 50%;
  background-color: #fbbc05;
}

.strength-bar.good {
  width: 75%;
  background-color: #4285f4;
}

.strength-bar.excellent {
  width: 100%;
  background-color: #34a853;
}

.strength-text {
  font-size: 0.75rem;
  font-weight: 500;
}

.password-requirements {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0;
  font-size: 0.75rem;
  color: #5f6368;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.dark-mode .password-requirements {
  color: #9aa0a6;
}

.password-requirements li {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.password-requirements li i {
  font-size: 0.75rem;
}

.password-requirements li.met {
  color: #34a853;
}

/* Form Options */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0.5rem 0;
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.8125rem;
  color: #5f6368;
  user-select: none;
}

.dark-mode .checkbox-container {
  color: #9aa0a6;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 1px solid #dadce0;
  border-radius: 4px;
  position: relative;
  transition: all 0.3s;
}

.dark-mode .checkmark {
  border-color: #3c4043;
}

.checkbox-container input:checked ~ .checkmark {
  background-color: #4285f4;
  border-color: #4285f4;
}

.dark-mode .checkbox-container input:checked ~ .checkmark {
  background-color: #8ab4f8;
  border-color: #8ab4f8;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
  left: 5px;
  top: 2px;
  width: 4px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.terms-group {
  margin: 0.5rem 0;
}

/* Buttons */
.auth-btn {
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.auth-btn.primary {
  background-color: #4285f4;
  color: white;
  border: none;
}

.auth-btn.primary:hover:not(:disabled) {
  background-color: #3367d6;
  transform: translateY(-1px);
}

.auth-btn.primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.dark-mode .auth-btn.primary {
  background-color: #8ab4f8;
  color: #202124;
}

.dark-mode .auth-btn.primary:hover:not(:disabled) {
  background-color: #7aa4e8;
}

.auth-btn.google-btn {
  background-color: white;
  color: #202124;
  border: 1px solid #dadce0;
}

.auth-btn.google-btn:hover {
  background-color: #f1f3f4;
}

.dark-mode .auth-btn.google-btn {
  background-color: #2d2d2d;
  border-color: #3c4043;
  color: #e8eaed;
}

.dark-mode .auth-btn.google-btn:hover {
  background-color: #3c4043;
}

.auth-btn.google-btn img {
  width: 18px;
  height: 18px;
}

/* Divider */
.auth-divider {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0.5rem 0;
}

.auth-divider:before,
.auth-divider:after {
  content: "";
  flex: 1;
  height: 1px;
  background-color: #dadce0;
}

.dark-mode .auth-divider:before,
.dark-mode .auth-divider:after {
  background-color: #3c4043;
}

.auth-divider span {
  font-size: 0.8125rem;
  color: #5f6368;
}

.dark-mode .auth-divider span {
  color: #9aa0a6;
}

/* Links */
.auth-link {
  color: #4285f4;
  text-decoration: none;
  font-size: 0.8125rem;
  transition: color 0.3s;
}

.auth-link:hover {
  color: #3367d6;
  text-decoration: underline;
}

.dark-mode .auth-link {
  color: #8ab4f8;
}

.dark-mode .auth-link:hover {
  color: #7aa4e8;
}

.auth-switch-text {
  text-align: center;
  font-size: 0.875rem;
  color: #5f6368;
  margin: 0.5rem 0 0;
}

.dark-mode .auth-switch-text {
  color: #9aa0a6;
}

/* Verification Code */
.verification-code {
  margin-top: 1rem;
}

.verification-code p {
  font-size: 0.8125rem;
  color: #5f6368;
  margin-bottom: 0.75rem;
}

.dark-mode .verification-code p {
  color: #9aa0a6;
}

.code-inputs {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.code-input {
  width: 40px;
  height: 48px;
  text-align: center;
  font-size: 1.25rem;
  border-radius: 8px;
  border: 1px solid #dadce0;
  transition: all 0.3s;
}

.code-input:focus {
  outline: none;
  border-color: #4285f4;
  box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2);
}

.code-input.error {
  border-color: #ea4335;
  animation: shake 0.5s;
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  20%,
  60% {
    transform: translateX(-5px);
  }
  40%,
  80% {
    transform: translateX(5px);
  }
}

.dark-mode .code-input {
  background-color: #2d2d2d;
  border-color: #3c4043;
  color: #e8eaed;
}

.dark-mode .code-input:focus {
  border-color: #8ab4f8;
  box-shadow: 0 0 0 2px rgba(138, 180, 248, 0.2);
}

.dark-mode .code-input.error {
  border-color: #ea4335;
}

/* Spinner */
.auth-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.dark-mode .auth-spinner {
  border-top-color: #202124;
}

/* Messages */
.auth-message {
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.8125rem;
  text-align: center;
}

.auth-message.success {
  background-color: rgba(52, 168, 83, 0.1);
  color: #34a853;
}

.auth-message.error {
  background-color: rgba(234, 67, 53, 0.1);
  color: #ea4335;
}

.auth-message.info {
  background-color: rgba(66, 133, 244, 0.1);
  color: #4285f4;
}

.dark-mode .auth-message.success {
  background-color: rgba(52, 168, 83, 0.2);
}

.dark-mode .auth-message.error {
  background-color: rgba(234, 67, 53, 0.2);
}

.dark-mode .auth-message.info {
  background-color: rgba(66, 133, 244, 0.2);
}

/* Responsive Adjustments */
@media (max-width: 480px) {
  .auth-modal-container {
    padding: 1.5rem;
  }

  .auth-form h2 {
    font-size: 1.25rem;
  }

  .code-input {
    width: 36px;
    height: 44px;
    font-size: 1rem;
  }
}
</style>
