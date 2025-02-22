<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">
      <!-- Close Button -->
      <button class="close-btn" @click="closeModal">✖</button>

      <!-- Login Form -->
      <div v-if="isLogin">
        <h1 class="injustifyLogoR">
          <ion-icon name="musical-note-outline"></ion-icon>Injustify
          <ion-icon name="musical-note-outline"></ion-icon>
        </h1>
        <div id="logininjustify">
          <h2>Login</h2>
          <form @submit.prevent="login">
            <input v-model="userEmail" type="email" placeholder="Email" required />
            <div class="passwordInputs">
              <input v-model="userPassword" type="password" placeholder="Password" required />
              <div class="showHidePassword" @click="togglePasswordVisibility">
                <i class="fa-solid fa-eye"></i>
              </div>
            </div>
            <button type="submit">Login</button>
            <div v-if="loading">
              <div class="loader"></div>
            </div>
            <label>
              <input type="checkbox" v-model="rememberMe" />
              Remember Me
            </label>
          </form>
          <div class="googleLogin" @click="authWithGoogle">
            <span>Login with;</span>
            <img src="../assets/google_logo.png" alt="Google Logo" />
          </div>
          <p>Forgot Password? <a href="#">Reset Password</a></p>
          <p>Don't have an account? <a @click="switchMode">Sign up</a></p>
        </div>
      </div>

      <!-- Signup Form -->
      <div v-else>
        <h1 class="injustifyLogoR">
          <ion-icon name="musical-note-outline"></ion-icon>Injustify
          <ion-icon name="musical-note-outline"></ion-icon>
        </h1>        <div id="signupinjustify">
          <h2>Sign Up</h2>
          <form @submit.prevent="signup">
            <input v-model="signupEmail" type="email" placeholder="Email" required />
            <input v-model="signupUsername" type="text" placeholder="Username" required />
            <div class="passwordInputs">
              <input v-model="signupPassword" type="password" placeholder="Password" required />
              <div class="showHidePassword" @click="togglePasswordVisibility">
                <i class="fa-solid fa-eye"></i>
              </div>
            </div>
            <div class="passwordInputs">
              <input v-model="signupConfirmPassword" type="password" placeholder="Confirm Password" required />
              <div class="showHidePassword" @click="togglePasswordVisibility">
                <i class="fa-solid fa-eye"></i>
              </div>
            </div>
            <button type="submit">Sign Up</button>
            <div v-if="loading">
              <div class="loader"></div>
            </div>
          </form>
          <div class="googleLogin" @click="authWithGoogle">
            <span>Signup with;</span>
            <img src="../assets/google_logo.png" alt="Google Logo" />
          </div>
          <label>
            <input type="checkbox" v-model="termsAccepted" required />
            I agree to the <a href="#">Terms and Conditions</a>
          </label>
          <p>Already have an account? <a @click="switchMode">Login</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/store';
import { SIGN_UP,AUTH_WITH_GOOGLE, MANUAL_LOGIN} from "@/utils";


export default {
  props: {
    isOpen: Boolean,
    onCloseModal: Function,
    isDarkMode: Boolean,
  },
  data() {
    return {
      userEmail: '',
      userPassword: '',
      signupEmail: '',
      signupUsername: '',
      signupPassword: '',
      signupConfirmPassword: '',
      rememberMe: false,
      termsAccepted: false,
      isLogin: true,
      loading: false,
      message: '',
      success: false,
    };
  },
  methods: {
    authWithGoogle(){
      window.location.href=AUTH_WITH_GOOGLE;
    },
    async login() {
      if (!this.userEmail || !this.userPassword) {
        this.showMessage('Please fill in all fields!', false);
        return;
      }
      
      this.loading = true;
      try {
        const response = await axios.post(MANUAL_LOGIN, {
          email: this.userEmail,
          password: this.userPassword,
        });
        
        this.showMessage('Login successful!', true);
        if (response.data.user) {
          const userStore = useUserStore();
          userStore.setUser(response.data.user);
          this.loading = false;
        }
        
        console.log('Backend response:', response.data);
        this.closeModal();
      } catch (error) {
        this.showMessage('Login failed. Check your credentials.', false);
        console.error('Login error:', error);
      }
      this.loading = false;
    },
    
    async signup() {
      if (!this.signupEmail || !this.signupUsername || !this.signupPassword || !this.signupConfirmPassword) {
        this.showMessage('Please fill in all fields!', false);
        return;
      }
      
      if (this.signupPassword !== this.signupConfirmPassword) {
        this.showMessage('Passwords do not match!', false);
        return;
      }
      
      this.loading = true;
      try {
        const response = await axios.post(SIGN_UP, {
          email: this.signupEmail,
          username: this.signupUsername,
          password: this.signupPassword,
        });
        
        this.showMessage('Signup successful!', true);
        if (response.data.user) {
          const userStore = useUserStore();
          userStore.setUser(response.data.user);
          this.loading = false;
        }
        
        console.log('Backend response:', response.data);
        this.closeModal();
      } catch (error) {
        this.showMessage('Signup failed. Try again.', false);
        console.error('Signup error:', error);
      }
      this.loading = false;
    },
    
    switchMode() {
      this.isLogin = !this.isLogin;
      this.message = '';
    },
    
    closeModal() {
      console.log('Close modal button clicked');
      this.$emit('close');
    },
    
    showMessage(message, success) {
      this.message = message;
      this.success = success;
    },
    togglePasswordVisibility(event) {
      let inputField = event.target.closest('.passwordInputs').querySelector('input');
      inputField.type = inputField.type === 'password' ? 'text' : 'password';
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.dark-mode {
  background: #333;
  color: white;
}
.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}
</style>


  
  <style scoped>
  /* 🔷 Modal Background */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    animation: fadeIn 0.3s ease-in-out;
  }
  

  
  
  /* 🔷 Close Button */
  .close-btn {
    position: absolute;
    top: 10px;
    right: 15px;
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }
  
  /* 🔷 Modal Title */
  .modal-title {
    font-size: 24px;
    margin-bottom: 15px;
    color: #333;
  }
  
  /* 🔷 Input Fields */
  input {
    width: 100%;
    padding: 10px;
    margin: 8px 0;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  /* 🔷 Buttons */
  .modal-btn {
    width: 100%;
    background: #007bff;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
    margin-top: 10px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .modal-btn:hover {
    background: #0056b3;
  }
  
  /* 🔷 Switch Mode Link */
  .switch-text {
    margin-top: 10px;
  }
  
  .switch-text a {
    color: #007bff;
    cursor: pointer;
    text-decoration: none;
    font-weight: bold;
  }
  
  .switch-text a:hover {
    text-decoration: underline;
  }
  .googleLogin img{
    width: 100px;
    border-radius: 10px;
    cursor: pointer;
}
 .googleLogin img:hover{
    background-color: rgba(128, 128, 128, 0.115);
}

.passwordInputs{
    position: relative;
    width: 100%;
}
.passwordInputs .showHidePassword{
    position: absolute;
    top: 50%;
    right: 0px;
    transform: translateY(-50%);
    cursor: pointer;
    color: gray;
    padding: 3px 2px;
}

.passwordInputs .showHidePassword:hover{
    color: rgb(40, 35, 35);
}

.passwordInputs input[type="password"]{
    padding-right: 40px !important;    
}

input[type='password'],
  input[type='text'],
  input[type='email']{
    box-sizing: border-box;
  }
  /* 🔷 Animations */
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes slideIn {
    from { transform: translateY(-20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }
  .injustifyLogoR{
    top: 0;
    left: 1px;
    font-size: 18px;

  }
  
  </style>
  
  

  
  <style scoped>
  /* 🔷 Modal Background */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    animation: fadeIn 0.3s ease-in-out;
  }
  
  /* 🔷 Modal Box */
  .modal-container {
    background-image: url(../assets/outerSpaceTerrain.jpg);
    
    padding: 25px;
    border-radius: 10px;
    width: 350px;
    text-align: center;
    position: relative;
    animation: slideIn 0.3s ease-in-out;
    background-size: cover;
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 10px;
    box-sizing: border-box;
    transition:  all 0.3s ease;
    opacity: 1;
    transform: translateY(0);
    color: white !important;
  }
  
  
  /* 🔷 Close Button */
  .close-btn {
    position: absolute;
    top: 10px;
    right: 15px;
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }
  
  /* 🔷 Modal Title */
  .modal-title {
    font-size: 24px;
    margin-bottom: 15px;
    color: #333;
  }
  
  /* 🔷 Input Fields */
  input {
    width: 100%;
    padding: 10px;
    margin: 8px 0;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  /* 🔷 Buttons */
  .modal-btn {
    width: 100%;
    background: #007bff;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
    margin-top: 10px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .modal-btn:hover {
    background: #0056b3;
  }
  
  /* 🔷 Switch Mode Link */
  .switch-text {
    margin-top: 10px;
  }
  
  .switch-text a {
    color: #007bff;
    cursor: pointer;
    text-decoration: none;
    font-weight: bold;
  }
  
  .switch-text a:hover {
    text-decoration: underline;
  }
  
  /* 🔷 Animations */
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes slideIn {
    from { transform: translateY(-20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }
  </style>
  