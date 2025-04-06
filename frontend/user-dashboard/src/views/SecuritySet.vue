<template>
  <div class="security-container">
    <h2>Security</h2>

    <div class="security-sections">
      <!-- Password and Security -->
      <div class="security-card" :class="{ darkmode3: isDarkMode }">
        <h3>Password and Security</h3>

        <div class="input-group">
          <label for="oldPassword">Old Password:</label>
          <input
            type="password"
            id="oldPassword"
            v-model="oldPassword"
            placeholder="Enter old password"
          />
        </div>
        <p class="notifier">Enter your current password before changing.</p>

        <div class="input-group">
          <label for="newPassword">New Password:</label>
          <input
            type="password"
            id="newPassword"
            v-model="newPassword"
            placeholder="Enter new password"
          />
        </div>
        <p class="notifier">Choose a strong password!</p>

        <div class="input-group">
          <label for="confirmPassword">Confirm New Password:</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            placeholder="Confirm new password"
          />
        </div>
        <p class="notifier">Ensure both passwords match.</p>

        <button @click="changePassword">Save Password</button>

        <div class="input-group">
          <label for="securityLevel">Security Level:</label>
          <select id="securityLevel" v-model="securityLevel">
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>
      </div>

      <!-- Two-Factor Authentication -->
      <div class="security-card" :class="{ darkmode3: isDarkMode }">
        <h3>Two-Factor Authentication</h3>

        <div class="toggle-group">
          <label>Enable 2FA:</label>
          <input type="checkbox" v-model="enableTwoFactor" />
        </div>

        <button v-if="enableTwoFactor" @click="generateCode">Generate Code</button>

        <div v-if="enableTwoFactor">
          <label>Code:</label>
          <input type="text" v-model="twoFactorCode" placeholder="Enter generated code" />

          <button @click="verifyCode">Verify Code</button>
        </div>
      </div>

      <!-- Account Deletion -->
      <div class="security-card" :class="{ darkmode3: isDarkMode }">
        <h4>Delete Account</h4>
        <p>This action is irreversible. Are you sure?</p>

        <button @click="showDeleteAccountCard = true">Delete Account</button>
      </div>
    </div>

    <!-- Delete Account Modal -->
    <div v-if="showDeleteAccountCard" class="delete-modal">
      <div class="delete-card" :class="{ darkmode3: isDarkMode }">
        <span class="close-btn" @click="showDeleteAccountCard = false">x</span>
        <h4>Delete Account</h4>
        <p class="warn-delete">Are you sure you want to delete this account?</p>

        <div class="profile-info">
          <img :src="profilePic" class="circular-profile-pic" alt="Profile Pic" />
          <h3>{{userName}}</h3>
          <p>{{formatDate(created_at)}}</p>

          <div class="email-card" :class="{ darkmode4: isDarkMode }">
            <span class="email-text">{{email}}</span>
            <i v-if="isverified" class="fas fa-check-circle"></i> <span>Verified</span>
          </div>

          <div>Shadows: <span>3000</span></div>
        </div>

        <p class="warn-delete">{{ msg }}</p>
        <input
          type="password"
          v-model="deleteAccountPassword"
          placeholder="Enter password"
        />
        <button @click="deleteAccount" :disabled="deleteAccountPassword === ''">
          Delete Account
        </button>
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

  props: {
    currentView: String,
  },
  data() {
    const userStore = useUserStore();

    return {
      oldPassword: "",
      newPassword: "",
      confirmPassword: "",
      securityLevel: "medium",
      enableTwoFactor: false,
      twoFactorCode: "",
      showDeleteAccountCard: false,
      deleteAccountPassword: "",
      isDarkMode: computed(() => userStore.isdarkmode),
      email: computed(() => userStore.email),
      userName:computed(() => userStore.name),
      isverified: computed(() => userStore.verifiedEmail),
      profilePic: computed(() => userStore.profilePic),
      emailVerified: computed(() => userStore.emailVerified),
      shadows: computed(() => userStore.shadows),
      userId: computed(() => userStore.userId),
      created_at:computed(() => userStore.created_at),
      msg: "Enter your password to confirm deletion:",
      userStore:useUserStore(),
      formatDate
    };
  },
  methods: {
    changePassword() {
      if (this.newPassword === this.confirmPassword) {
        alert("Password changed successfully!");
      } else {
        alert("Passwords do not match.");
      }
    },
    generateCode() {
      this.twoFactorCode = Math.floor(100000 + Math.random() * 900000).toString();
      alert(`Your 2FA code: ${this.twoFactorCode}`);
    },
    verifyCode() {
      alert("Code verified successfully!");
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
            this.userStore.set_snackbarMessage(
          "Account Deleted successfully, will'll miss you!",
          "success",
          10000
        );
          } else {
            this.msg = response.data.detail;
            this.userStore.set_snackbarMessage(
              "Failed to delete account, please try again later.",
              "error",
              10000
            );
          }
        })
        .catch((error) => {
          console.error("Error deleting account1", error.response.data.detail);
          this.msg = error.response.data.detail;
          this.userStore.set_snackbarMessage(
            "Failed to delete account, please try again later.",
            "error",
            10000
          );
        });
    },
  },
};
</script>

<style scoped>
.darkmode4 {
  background: #555353 !important;
  color: #ffffff;
}
.darkmode3 {
  background: #777575 !important;
  color: #ffffff;
}
.security-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.security-card {
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

/* Input Groups */
.input-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.input-group label {
  font-weight: bold;
}

.input-group input,
.input-group select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Notifiers */
.notifier {
  font-size: 12px;
  color: gray;
}

/* Buttons */
button {
  width: 100%;
  padding: 10px;
  border: none;
  background: #3498db;
  color: white;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Delete Modal */
.delete-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.819);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.delete-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: 350px;
}

.close-btn {
  float: right;
  cursor: pointer;
  font-size: 20px;
}

.warn-delete {
  color: red;
  font-weight: bold;
}

/* Profile Info */
.profile-info {
  text-align: center;
  margin-top: 10px;
}

.circular-profile-pic {
  min-width: 60px;
  min-height: 60px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: gray;
}

.email-card {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
  font-size: 14px;
  background: #f4f4f4;
  padding: 5px;
  border-radius: 5px;
}
</style>
