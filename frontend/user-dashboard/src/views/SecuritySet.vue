<template>
  <div class="security-container" :class="{ 'dark-mode': isDarkMode }">
    <div class="security-header">
      <h2 class="security-title">
        <i class="fas fa-shield-alt"></i> Account Security
      </h2>
      <div class="security-status">
        <div class="status-indicator" :class="securityLevel">
          <i class="fas" :class="securityLevelIcon"></i>
          {{ securityLevelLabel }} Security
        </div>
      </div>
    </div>

    <div class="security-grid">
      <!-- Password Management Card -->
      <div class="security-card">
        <div class="card-header">
          <i class="fas fa-key"></i>
          <h3>Password Management</h3>
        </div>

        <div class="password-strength" v-if="newPassword">
          <div class="strength-meter">
            <div class="strength-bar" :class="passwordStrengthClass"></div>
          </div>
          <span class="strength-text">{{ passwordStrengthText }}</span>
        </div>

        <div class="input-group">
          <label for="oldPassword">
            <i class="fas fa-lock"></i> Current Password
          </label>
          <div class="password-input">
            <input
              type="password"
              id="oldPassword"
              v-model="oldPassword"
              placeholder="Enter current password"
              class="modern-input"
              :class="{ 'error': passwordError }"
            />
            <button class="input-action" @click="togglePasswordVisibility('oldPassword')">
              <i class="fas" :class="showOldPassword ? 'fa-eye-slash' : 'fa-eye'"></i>
            </button>
          </div>
          <p class="input-hint">Enter your current password to make changes</p>
        </div>

        <div class="input-group">
          <label for="newPassword">
            <i class="fas fa-key"></i> New Password
          </label>
          <div class="password-input">
            <input
              type="password"
              id="newPassword"
              v-model="newPassword"
              placeholder="Create new password"
              class="modern-input"
              :class="{ 'error': passwordError }"
              @input="checkPasswordStrength"
            />
            <button class="input-action" @click="togglePasswordVisibility('newPassword')">
              <i class="fas" :class="showNewPassword ? 'fa-eye-slash' : 'fa-eye'"></i>
            </button>
          </div>
          <ul class="password-requirements">
            <li :class="{ 'met': hasMinLength }">
              <i class="fas" :class="hasMinLength ? 'fa-check-circle' : 'fa-circle'"></i>
              At least 8 characters
            </li>
            <li :class="{ 'met': hasUpperCase }">
              <i class="fas" :class="hasUpperCase ? 'fa-check-circle' : 'fa-circle'"></i>
              At least 1 uppercase letter
            </li>
            <li :class="{ 'met': hasNumber }">
              <i class="fas" :class="hasNumber ? 'fa-check-circle' : 'fa-circle'"></i>
              At least 1 number
            </li>
            <li :class="{ 'met': hasSpecialChar }">
              <i class="fas" :class="hasSpecialChar ? 'fa-check-circle' : 'fa-circle'"></i>
              At least 1 special character
            </li>
          </ul>
        </div>

        <div class="input-group">
          <label for="confirmPassword">
            <i class="fas fa-redo"></i> Confirm New Password
          </label>
          <div class="password-input">
            <input
              type="password"
              id="confirmPassword"
              v-model="confirmPassword"
              placeholder="Re-enter new password"
              class="modern-input"
              :class="{ 'error': passwordMismatch }"
            />
            <button class="input-action" @click="togglePasswordVisibility('confirmPassword')">
              <i class="fas" :class="showConfirmPassword ? 'fa-eye-slash' : 'fa-eye'"></i>
            </button>
          </div>
          <p class="input-hint" :class="{ 'error-text': passwordMismatch }">
            {{ passwordMismatch ? 'Passwords do not match' : 'Both passwords must match' }}
          </p>
        </div>

        <div class="security-level-selector">
          <label>
            <i class="fas fa-shield-alt"></i> Security Level
          </label>
          <div class="level-options">
            <label 
              v-for="level in securityLevels" 
              :key="level.value"
              :class="{ 'active': securityLevel === level.value }"
            >
              <input 
                type="radio" 
                v-model="securityLevel" 
                :value="level.value"
              >
              <div class="level-card">
                <i :class="level.icon"></i>
                <span class="level-name">{{ level.name }}</span>
                <span class="level-desc">{{ level.desc }}</span>
              </div>
            </label>
          </div>
        </div>

        <button 
          class="save-btn" 
          @click="changePassword"
          :disabled="!canChangePassword"
        >
          <i class="fas fa-save"></i> Update Password
        </button>
      </div>

      <!-- Two-Factor Authentication Card -->
      <div class="security-card">
        <div class="card-header">
          <i class="fas fa-mobile-alt"></i>
          <h3>Two-Factor Authentication</h3>
          <div class="status-badge" :class="{ 'active': enableTwoFactor }">
            {{ enableTwoFactor ? 'Enabled' : 'Disabled' }}
          </div>
        </div>

        <div class="two-factor-content">
          <div class="two-factor-description">
            <p>Add an extra layer of security to your account. When enabled, you'll be required to enter both your password and a verification code from your mobile device when logging in.</p>
            <div class="security-benefits">
              <div class="benefit-item">
                <i class="fas fa-check-circle"></i>
                <span>Protects against password theft</span>
              </div>
              <div class="benefit-item">
                <i class="fas fa-check-circle"></i>
                <span>Required for sensitive actions</span>
              </div>
              <div class="benefit-item">
                <i class="fas fa-check-circle"></i>
                <span>Supports authenticator apps</span>
              </div>
            </div>
          </div>

          <div class="toggle-group">
            <label class="toggle-item large">
              <input 
                type="checkbox" 
                v-model="enableTwoFactor" 
                class="toggle-input"
                @change="handleTwoFactorToggle"
              >
              <span class="toggle-slider"></span>
              <span class="toggle-label">Enable Two-Factor Authentication</span>
            </label>
          </div>

          <div v-if="twoFactorSetup" class="two-factor-setup">
            <div class="qr-code-container">
              <div class="qr-placeholder">
                <i class="fas fa-qrcode"></i>
                <p>Scan this QR code with your authenticator app</p>
              </div>
              <div class="setup-codes">
                <p class="setup-instruction">Or enter this code manually:</p>
                <div class="manual-code">JBSW Y3DP EHPK 3PXP</div>
                <p class="setup-instruction">Then enter the verification code below:</p>
                
                <div class="verification-input">
                  <input 
                    type="text" 
                    v-model="twoFactorCode" 
                    placeholder="6-digit code"
                    maxlength="6"
                    class="modern-input"
                  >
                  <button 
                    class="verify-btn"
                    @click="verifyCode"
                    :disabled="!twoFactorCode || twoFactorCode.length < 6"
                  >
                    Verify
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Account Activity Card -->
      <div class="security-card">
        <div class="card-header">
          <i class="fas fa-clock"></i>
          <h3>Recent Activity</h3>
        </div>

        <div class="activity-list">
          <div class="activity-item" v-for="(activity, index) in recentActivity" :key="index">
            <div class="activity-icon" :class="activity.type">
              <i :class="activity.icon"></i>
            </div>
            <div class="activity-details">
              <div class="activity-description">{{ activity.description }}</div>
              <div class="activity-meta">
                <span class="activity-time">{{ activity.time }}</span>
                <span class="activity-location">
                  <i class="fas fa-map-marker-alt"></i> {{ activity.location }}
                </span>
              </div>
            </div>
            <button 
              class="activity-action"
              @click="reviewActivity(activity)"
              v-if="activity.action"
            >
              {{ activity.action }}
            </button>
          </div>
        </div>

        <button class="view-all-btn">
          <i class="fas fa-history"></i> View All Activity
        </button>
      </div>

      <!-- Account Deletion Card -->
      <div class="security-card danger-zone">
        <div class="card-header">
          <i class="fas fa-exclamation-triangle"></i>
          <h3>Danger Zone</h3>
        </div>

        <div class="danger-content">
          <p class="warning-message">
            <i class="fas fa-exclamation-circle"></i>
            These actions are irreversible. Proceed with caution.
          </p>

          <div class="danger-action">
            <div class="action-description">
              <h4>Delete Account</h4>
              <p>Permanently remove your account and all associated data from our servers.</p>
            </div>
            <button 
              class="danger-btn"
              @click="showDeleteAccountModal = true"
            >
              <i class="fas fa-trash-alt"></i> Delete Account
            </button>
          </div>

          <div class="danger-action">
            <div class="action-description">
              <h4>Delete All Data</h4>
              <p>Remove all your personal data while keeping your account active.</p>
            </div>
            <button class="danger-btn">
              <i class="fas fa-eraser"></i> Delete Data
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Account Modal -->
    <div v-if="showDeleteAccountModal" class="security-modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>
            <i class="fas fa-exclamation-triangle"></i>
            Delete Account Permanently
          </h3>
          <button class="close-btn" @click="showDeleteAccountModal = false">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <div class="modal-body">
          <div class="account-summary">
            <img :src="profilePic" class="profile-avatar" alt="Profile" />
            <div class="account-details">
              <h4>{{ userName }}</h4>
              <div class="account-meta">
                <span class="meta-item">
                  <i class="fas fa-envelope"></i> {{ email }}
                  <i v-if="isVerified" class="fas fa-check-circle verified"></i>
                </span>
                <span class="meta-item">
                  <i class="fas fa-calendar-alt"></i> Member since {{ formatDate(created_at) }}
                </span>
              </div>
            </div>
          </div>

          <div class="deletion-warning">
            <div class="warning-icon">
              <i class="fas fa-exclamation-circle"></i>
            </div>
            <div class="warning-content">
              <h4>This action cannot be undone</h4>
              <p>All of your data including playlists, favorites, and history will be permanently deleted. You won't be able to recover any information.</p>
            </div>
          </div>

          <div class="confirmation-step">
            <p>To confirm, please enter your password:</p>
            <div class="password-input">
              <input
                type="password"
                v-model="deleteAccountPassword"
                placeholder="Enter your password"
                class="modern-input"
                :class="{ 'error': deleteError }"
              />
              <button class="input-action" @click="togglePasswordVisibility('deletePassword')">
                <i class="fas" :class="showDeletePassword ? 'fa-eye-slash' : 'fa-eye'"></i>
              </button>
            </div>
            <p class="error-message" v-if="deleteError">{{ deleteError }}</p>
          </div>
        </div>

        <div class="modal-footer">
          <button 
            class="cancel-btn"
            @click="showDeleteAccountModal = false"
          >
            Cancel
          </button>
          <button 
            class="confirm-delete-btn"
            @click="deleteAccount"
            :disabled="!deleteAccountPassword"
          >
            <i class="fas fa-trash-alt"></i> Delete Account Permanently
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "@/store/index.js";
import { computed } from "vue";
import axios from "axios";
import { BASE_URL,formatDate } from "@/utils/index.js";


export default {
  name: "SecuritySettings",

  data() {
    const userStore = useUserStore();

    return {
      oldPassword: '',
      newPassword: '',
      confirmPassword: '',
      passwordError: false,
      passwordMismatch: false,
      showOldPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
      showDeletePassword: false,
      passwordStrength: 0,
      enableTwoFactor: false,
      twoFactorSetup: false,
      twoFactorCode: '',
      securityLevel: 'medium',
      showDeleteAccountModal: false,
      deleteAccountPassword: '',
      deleteError: '',
      isDarkMode: computed(() => userStore.isdarkmode),
      email: computed(() => userStore.email),
      userName:computed(() => userStore.name),
      isverified: computed(() => userStore.verifiedEmail),
      profilePic: computed(() => userStore.profilePic),
      emailVerified: computed(() => userStore.emailVerified),
      shadows: computed(() => userStore.shadows),
      userId: computed(() => userStore.userId),
      created_at:computed(() => userStore.created_at),
      useStore: useUserStore(),
      formatDate,
      recentActivity: [
        {
          type: 'login',
          icon: 'fas fa-sign-in-alt',
          description: 'Successful login from new device',
          time: '2 hours ago',
          location: 'New York, NY',
          action: 'Review'
        },
        {
          type: 'password',
          icon: 'fas fa-key',
          description: 'Password changed',
          time: '1 week ago',
          location: 'Chicago, IL'
        },
        {
          type: 'device',
          icon: 'fas fa-mobile-alt',
          description: 'New device authorized',
          time: '2 weeks ago',
          location: 'San Francisco, CA',
          action: 'Review'
        }
      ],
      securityLevels: [
        {
          value: 'low',
          name: 'Basic',
          desc: 'Standard security',
          icon: 'fas fa-shield-alt'
        },
        {
          value: 'medium',
          name: 'Enhanced',
          desc: 'Additional verification',
          icon: 'fas fa-shield-virus'
        },
        {
          value: 'high',
          name: 'Maximum',
          desc: 'Strict protection',
          icon: 'fas fa-lock'
        }
      ]
    }
  },
  computed: {
    canChangePassword() {
      return (
        this.oldPassword &&
        this.newPassword &&
        this.confirmPassword &&
        this.newPassword === this.confirmPassword &&
        this.passwordStrength >= 2
      )
    },
    hasMinLength() {
      return this.newPassword.length >= 8
    },
    hasUpperCase() {
      return /[A-Z]/.test(this.newPassword)
    },
    hasNumber() {
      return /[0-9]/.test(this.newPassword)
    },
    hasSpecialChar() {
      return /[!@#$%^&*(),.?":{}|<>]/.test(this.newPassword)
    },
    passwordStrengthClass() {
      if (this.passwordStrength === 0) return 'weak'
      if (this.passwordStrength === 1) return 'fair'
      if (this.passwordStrength === 2) return 'good'
      return 'excellent'
    },
    passwordStrengthText() {
      if (this.passwordStrength === 0) return 'Weak'
      if (this.passwordStrength === 1) return 'Fair'
      if (this.passwordStrength === 2) return 'Good'
      return 'Excellent'
    },
    securityLevelLabel() {
      const level = this.securityLevels.find(l => l.value === this.securityLevel)
      return level ? level.name : ''
    },
    securityLevelIcon() {
      if (this.securityLevel === 'low') return 'fa-shield-alt'
      if (this.securityLevel === 'medium') return 'fa-shield-virus'
      return 'fa-lock'
    }
  },
  methods: {
    togglePasswordVisibility(field) {
      if (field === 'oldPassword') this.showOldPassword = !this.showOldPassword
      if (field === 'newPassword') this.showNewPassword = !this.showNewPassword
      if (field === 'confirmPassword') this.showConfirmPassword = !this.showConfirmPassword
      if (field === 'deletePassword') this.showDeletePassword = !this.showDeletePassword
    },
    checkPasswordStrength() {
      let strength = 0
      if (this.newPassword.length >= 8) strength++
      if (/[A-Z]/.test(this.newPassword)) strength++
      if (/[0-9]/.test(this.newPassword)) strength++
      if (/[!@#$%^&*(),.?":{}|<>]/.test(this.newPassword)) strength++
      this.passwordStrength = strength
    },
    changePassword() {
      // Password change logic
      console.log('Password changed')
    },
    handleTwoFactorToggle() {
      if (this.enableTwoFactor) {
        this.twoFactorSetup = true
        // Generate 2FA code logic
      } else {
        this.twoFactorSetup = false
      }
    },
    generateCode() {
      // Code generation logic
      console.log('2FA code generated')
    },
    verifyCode() {
      // Code verification logic
      console.log('Code verified')
    },
    deleteAccount() {
      if (!this.userId && !this.deleteAccountPassword) {
        return;
      }
      if(!confirm(`confirm to delete account for ${this.email} from Injustify`))return;

      axios
        .post(`${BASE_URL}/account/delete`, {
          userId:this.userId,
          password:this.deleteAccountPassword,
        })
        .then((response) => {
          if (response.data.success) {
            this.userStore.setUser([])
            this.msg = response.data.message || response.data.detail;
            this.showDeleteAccountCard = false;
            this.useStore.set_snackbarMessage(
          "Account Deleted successfully, will'll miss you!",
          "success",
          10000
        );
          } else {
            this.msg = response.data.detail;
            this.useStore.set_snackbarMessage(
              "Failed to delete account, please try again later.",
              "error",
              10000
            );
          }
        })
        .catch((error) => {
          console.error("Error deleting account1", error.response);
          this.msg = error.response;
          this.useStore.set_snackbarMessage(
            "Failed to delete account, please try again later.",
            "error",
            10000
          );
        });
    },
  

    reviewActivity(activity) {
      console.log('Reviewing activity:', activity)
    }
  }
}
</script>

<style scoped>
/* Base Styles */
.security-container {
  --primary-color: #4285f4;
  --primary-light: #e8f0fe;
  --primary-dark: #3367d6;
  --text-primary: #202124;
  --text-secondary: #5f6368;
  --bg-color: #ffffff;
  --card-bg: #ffffff;
  --border-color: #dadce0;
  --hover-color: #f1f3f4;
  --success-color: #34a853;
  --error-color: #ea4335;
  --warning-color: #fbbc05;
  --danger-color: #d93025;
  --danger-light: #fce8e6;
  --low-color: #fbbc05;
  --medium-color: #4285f4;
  --high-color: #34a853;
  --login-color: #34a853;
  --password-color: #4285f4;
  --device-color: #fbbc05;
  font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', sans-serif;
  background-color: var(--bg-color);
  color: var(--text-primary);
  transition: all 0.3s ease;
}

/* Dark Mode */
.security-container.dark-mode {
  --primary-color: #8ab4f8;
  --primary-light: #202124;
  --text-primary: #e8eaed;
  --text-secondary: #9aa0a6;
  --bg-color: #121212;
  --card-bg: #1e1e1e;
  --border-color: #3c4043;
  --hover-color: #2d2d2d;
  --danger-light: #3c1a1a;
}

/* Layout */
.security-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.security-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--primary-color);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.security-status {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.status-indicator {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 500;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-indicator i {
  font-size: 1rem;
}

.status-indicator.low {
  background-color: rgba(251, 188, 5, 0.1);
  color: var(--low-color);
}

.status-indicator.medium {
  background-color: rgba(66, 133, 244, 0.1);
  color: var(--medium-color);
}

.status-indicator.high {
  background-color: rgba(52, 168, 83, 0.1);
  color: var(--high-color);
}

.security-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.security-card {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
  transition: transform 0.2s, box-shadow 0.2s;
}

.security-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.security-card.danger-zone {
  border-left: 4px solid var(--danger-color);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  position: relative;
}

.card-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.card-header i {
  color: var(--primary-color);
  font-size: 1.25rem;
}

.danger-zone .card-header i {
  color: var(--danger-color);
}

.status-badge {
  position: absolute;
  right: 0;
  top: 0;
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  background-color: var(--border-color);
  color: var(--text-secondary);
}

.status-badge.active {
  background-color: var(--success-color);
  color: white;
}

/* Input Groups */
.input-group {
  margin-bottom: 1.5rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.modern-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background-color: var(--card-bg);
  color: var(--text-primary);
  font-size: 1rem;
  transition: border 0.3s, box-shadow 0.3s;
  box-sizing: border-box;
}

.modern-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2);
}

.modern-input.error {
  border-color: var(--error-color);
}

.modern-input.error:focus {
  box-shadow: 0 0 0 2px rgba(234, 67, 53, 0.2);
}

.input-hint {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 0.5rem;
}

.error-text {
  color: var(--error-color);
}

.password-input {
  position: relative;
}

.password-input .modern-input {
  padding-right: 40px;
}

.input-action {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s;
}

.input-action:hover {
  background-color: var(--hover-color);
  color: var(--primary-color);
}

/* Password Strength */
.password-strength {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.strength-meter {
  flex: 1;
  height: 6px;
  background-color: var(--border-color);
  border-radius: 3px;
  overflow: hidden;
}

.strength-bar {
  height: 100%;
  width: 0%;
  transition: width 0.3s, background-color 0.3s;
}

.strength-bar.weak {
  width: 25%;
  background-color: var(--error-color);
}

.strength-bar.fair {
  width: 50%;
  background-color: var(--low-color);
}

.strength-bar.good {
  width: 75%;
  background-color: var(--medium-color);
}

.strength-bar.excellent {
  width: 100%;
  background-color: var(--high-color);
}

.strength-text {
  font-size: 0.75rem;
  font-weight: 500;
  min-width: 60px;
  text-align: right;
}

.password-requirements {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0;
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.password-requirements li {
  margin-bottom: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.password-requirements li.met {
  color: var(--success-color);
}

.password-requirements li i {
  font-size: 0.875rem;
}

/* Security Level */
.security-level-selector {
  margin: 2rem 0;
}

.level-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 0.75rem;
  margin-top: 0.75rem;
}

.level-options label {
  position: relative;
  cursor: pointer;
}

.level-options input[type="radio"] {
  position: absolute;
  opacity: 0;
}

.level-card {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.level-options input[type="radio"]:checked + .level-card {
  border-color: var(--primary-color);
  background-color: var(--primary-light);
  color: var(--primary-color);
}

.level-options input[type="radio"]:hover + .level-card {
  border-color: var(--primary-color);
}

.level-card i {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.level-name {
  font-weight: 500;
  display: block;
}

.level-desc {
  font-size: 0.6875rem;
  color: var(--text-secondary);
  display: block;
}

.level-options input[type="radio"]:checked + .level-card .level-desc {
  color: var(--primary-color);
}

/* Two-Factor Authentication */
.two-factor-content {
  margin-top: 1rem;
}

.two-factor-description {
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--text-secondary);
}

.security-benefits {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
}

.benefit-item i {
  color: var(--success-color);
}

.toggle-group {
  margin: 1.5rem 0;
}

.toggle-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  position: relative;
}

.toggle-item.large {
  padding: 0.75rem;
  background-color: var(--primary-light);
  border-radius: 8px;
}

.toggle-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: relative;
  display: inline-block;
  width: 42px;
  height: 22px;
  background-color: var(--border-color);
  transition: .4s;
  border-radius: 22px;
  flex-shrink: 0;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

.toggle-input:checked + .toggle-slider {
  background-color: var(--primary-color);
}

.toggle-input:checked + .toggle-slider:before {
  transform: translateX(20px);
}

.toggle-label {
  flex: 1;
  font-size: 0.9375rem;
}

.two-factor-setup {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.qr-code-container {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.qr-placeholder {
  width: 160px;
  height: 160px;
  background-color: var(--bg-color);
  border: 1px dashed var(--border-color);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.qr-placeholder i {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  color: var(--primary-color);
}

.qr-placeholder p {
  font-size: 0.75rem;
  text-align: center;
  padding: 0 0.5rem;
}

.setup-codes {
  flex: 1;
}

.setup-instruction {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  margin: 0.5rem 0;
}

.manual-code {
  font-family: monospace;
  font-size: 1.25rem;
  letter-spacing: 1px;
  padding: 0.75rem;
  background-color: var(--bg-color);
  border-radius: 6px;
  margin: 0.75rem 0;
  text-align: center;
}

.verification-input {
  display: flex;
  gap: 0.5rem;
}

.verification-input .modern-input {
  flex: 1;
}

.verify-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.verify-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.verify-btn:hover:not(:disabled) {
  background-color: var(--primary-dark);
}

/* Activity List */
.activity-list {
  margin: 1rem 0;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-color);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-icon.login {
  background-color: rgba(52, 168, 83, 0.1);
  color: var(--login-color);
}

.activity-icon.password {
  background-color: rgba(66, 133, 244, 0.1);
  color: var(--password-color);
}

.activity-icon.device {
  background-color: rgba(251, 188, 5, 0.1);
  color: var(--device-color);
}

.activity-details {
  flex: 1;
}

.activity-description {
  font-size: 0.875rem;
  font-weight: 500;
}

.activity-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

.activity-action {
  background: transparent;
  border: none;
  color: var(--primary-color);
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.activity-action:hover {
  background-color: var(--primary-light);
}

.view-all-btn {
  background: transparent;
  border: none;
  color: var(--primary-color);
  font-weight: 500;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  transition: background-color 0.3s;
}

.view-all-btn:hover {
  background-color: var(--primary-light);
}

/* Danger Zone */
.danger-content {
  margin-top: 1rem;
}

.warning-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--danger-color);
  font-size: 0.875rem;
  padding: 0.75rem;
  background-color: var(--danger-light);
  border-radius: 6px;
  margin-bottom: 1.5rem;
}

.danger-action {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid var(--border-color);
}

.danger-action:last-child {
  border-bottom: none;
}

.action-description h4 {
  margin: 0 0 0.25rem;
  font-size: 0.9375rem;
}

.action-description p {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-secondary);
}

.danger-btn {
  background-color: transparent;
  color: var(--danger-color);
  border: 1px solid var(--danger-color);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s;
}

.danger-btn:hover {
  background-color: rgba(217, 48, 37, 0.1);
}

/* Modal Styles */
.security-modal {
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
}

.modal-content {
  background-color: var(--card-bg);
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--danger-color);
}

.close-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-size: 1.25rem;
  cursor: pointer;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s;
}

.close-btn:hover {
  background-color: var(--hover-color);
}

.modal-body {
  padding: 1.5rem;
}

.account-summary {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.profile-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
}

.account-details {
  flex: 1;
}

.account-details h4 {
  margin: 0;
  font-size: 1.125rem;
}

.account-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 0.5rem;
  font-size: 0.8125rem;
  color: var(--text-secondary);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.verified {
  color: var(--success-color);
}

.deletion-warning {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background-color: var(--danger-light);
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.warning-icon i {
  font-size: 1.5rem;
  color: var(--danger-color);
}

.warning-content h4 {
  margin: 0 0 0.5rem;
  color: var(--danger-color);
}

.warning-content p {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.5;
}

.confirmation-step {
  margin-top: 1.5rem;
}

.confirmation-step p {
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
}

.error-message {
  color: var(--error-color);
  font-size: 0.8125rem;
  margin-top: 0.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--border-color);
}

.cancel-btn {
  background-color: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-btn:hover {
  background-color: var(--hover-color);
}

.confirm-delete-btn {
  background-color: var(--danger-color);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.3s;
}

.confirm-delete-btn:hover:not(:disabled) {
  background-color: #c5221f;
}

.confirm-delete-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Buttons */
.save-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  justify-content: center;
  margin-top: 1rem;
}

.save-btn:hover:not(:disabled) {
  background-color: var(--primary-dark);
  transform: translateY(-1px);
}

.save-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .security-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .security-status {
    width: 100%;
    justify-content: flex-end;
  }
  
  .qr-code-container {
    flex-direction: column;
  }
  
  .qr-placeholder {
    width: 100%;
    height: auto;
    aspect-ratio: 1/1;
  }
}

@media (max-width: 480px) {
  .security-grid {
    grid-template-columns: 1fr;
  }
  
  .danger-action {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .cancel-btn,
  .confirm-delete-btn {
    width: 100%;
  }
}
</style>