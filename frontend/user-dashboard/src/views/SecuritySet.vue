<template>
  <div  class="security-container">
    <h2>Security</h2>

    <div class="security-sections">
      <!-- Password and Security -->
      <div class="security-card">
        <h3>Password and Security</h3>

        <div class="input-group">
          <label for="oldPassword">Old Password:</label>
          <input type="password" id="oldPassword" v-model="oldPassword" placeholder="Enter old password">
        </div>
        <p class="notifier">Enter your current password before changing.</p>

        <div class="input-group">
          <label for="newPassword">New Password:</label>
          <input type="password" id="newPassword" v-model="newPassword" placeholder="Enter new password">
        </div>
        <p class="notifier">Choose a strong password!</p>

        <div class="input-group">
          <label for="confirmPassword">Confirm New Password:</label>
          <input type="password" id="confirmPassword" v-model="confirmPassword" placeholder="Confirm new password">
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
      <div class="security-card">
        <h3>Two-Factor Authentication</h3>

        <div class="toggle-group">
          <label>Enable 2FA:</label>
          <input type="checkbox" v-model="enableTwoFactor">
        </div>

        <button v-if="enableTwoFactor" @click="generateCode">Generate Code</button>

        <div v-if="enableTwoFactor">
          <label>Code:</label>
          <input type="text" v-model="twoFactorCode" placeholder="Enter generated code">

          <button @click="verifyCode">Verify Code</button>
        </div>
      </div>

      <!-- Account Deletion -->
      <div class="security-card">
        <h4>Delete Account</h4>
        <p>This action is irreversible. Are you sure?</p>

        <button @click="showDeleteAccountCard = true">Delete Account</button>
      </div>
    </div>

    <!-- Delete Account Modal -->
    <div v-if="showDeleteAccountCard" class="delete-modal">
      <div class="delete-card">
        <span class="close-btn" @click="showDeleteAccountCard = false">x</span>
        <h4>Delete Account</h4>
        <p class="warn-delete">Are you sure you want to delete this account?</p>

        <div class="profile-info">
          <img src="" class="circular-profile-pic" alt="Profile Pic">
          <h3>John Doe</h3>
          <p>User since: March 2021</p>

          <div class="email-card">
            <span class="email-text">Kariuki12nicholas@gmail.com</span>
            <i class="fas fa-check-circle"></i> <span>Verified</span>
          </div>

          <div>Shadows: <span>3000</span></div>
        </div>

        <p class="warn-delete">Enter your password to confirm deletion:</p>
        <input type="password" v-model="deleteAccountPassword" placeholder="Enter password">
        <button @click="deleteAccount" :disabled="deleteAccountPassword === ''">Delete Account</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SecuritySettings",

  props: {
    currentView: String,
  },
  data() {
    return {
      oldPassword: '',
      newPassword: '',
      confirmPassword: '',
      securityLevel: 'medium',
      enableTwoFactor: false,
      twoFactorCode: '',
      showDeleteAccountCard: false,
      deleteAccountPassword: '',
    };
  },
  methods: {
    changePassword() {
      if (this.newPassword === this.confirmPassword) {
        alert('Password changed successfully!');
      } else {
        alert('Passwords do not match.');
      }
    },
    generateCode() {
      this.twoFactorCode = Math.floor(100000 + Math.random() * 900000).toString();
      alert(`Your 2FA code: ${this.twoFactorCode}`);
    },
    verifyCode() {
      alert('Code verified successfully!');
    },
    deleteAccount() {
      if (this.deleteAccountPassword) {
        alert('Account deleted successfully!');
        this.showDeleteAccountCard = false;
      }
    },
  },
};
</script>

<style scoped>
/* Security Page Container */
.security-container {
  width: 100%;
  max-width: 600px;
  margin: auto;
  padding: 20px;
  background: #f4f4f4;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

/* Sections */
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

.input-group input, .input-group select {
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
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
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
  width: 60px;
  height: 60px;
  border-radius: 50%;
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
