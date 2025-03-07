<template>
  <div class="main_tabs MainContainer" :class="{ collabsedBig: iscollapsedBig }">
    <div class="feedback-container">
      <div class="feedback-content">
        <h1 class="feedback-title">📝 We Value Your Feedback!</h1>
        <p class="feedback-subtitle">
          Let us know what you love, what needs fixing, or what could be improved.
        </p>

        <!-- Rating Section -->
        <div class="rating-container">
          <span
            v-for="star in 5"
            :key="star"
            class="star"
            :class="{ active: star <= rating }"
            @click="setRating(star)"
          >
            ★
          </span>
        </div>

        <!-- Feedback Form -->
        <form @submit.prevent="submitFeedback" class="feedback-form">
          <textarea
            v-model="feedbackText"
            placeholder="Share your thoughts..."
            @input="updateCharacterCount"
            class="feedback-input"
            maxlength="500"
          ></textarea>
          <p class="char-count">{{ charCount }}/500</p>

          <!-- Issue Reporting Section -->
          <h2 class="section-title">🔧 Report an Issue / Suggest an Improvement</h2>

          <label for="issueType">Issue Type:</label>
          <select v-model="issueType" class="dropdown">
            <option disabled value="">Select an issue type</option>
            <option value="bug">🐞 Bug</option>
            <option value="feature">🚀 Feature Request</option>
            <option value="performance">⚡ Performance Issue</option>
            <option value="ui">🎨 UI Improvement</option>
          </select>

          <label for="issueDesc">Describe the Issue:</label>
          <textarea
            v-model="issueDesc"
            placeholder="Explain the issue or feature request..."
            class="feedback-input"
            maxlength="500"
          ></textarea>

          <label for="priority">Priority Level:</label>
          <select v-model="priority" class="dropdown">
            <option disabled value="">Select priority</option>
            <option value="low">🟢 Low</option>
            <option value="medium">🟡 Medium</option>
            <option value="high">🔴 High</option>
          </select>

          <label for="fileUpload">Upload Screenshot (Optional):</label>
          <input type="file" @change="handleFileUpload" class="file-input" />

          <button :disabled="isDisabled" type="submit" class="submit-btn">
            🚀 Submit Feedback
          </button>
        </form>

        <!-- Success Message -->
        <p v-if="submitted" class="success-message">
          🎉 Thanks for your feedback! We appreciate it. 💙
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const feedbackText = ref("");
const issueType = ref("");
const issueDesc = ref("");
const priority = ref("");
const rating = ref(0);
const charCount = ref(0);
const submitted = ref(false);
const uploadedFile = ref(null);

const updateCharacterCount = () => {
  charCount.value = feedbackText.value.length;
};

const setRating = (star) => {
  rating.value = star;
};

const handleFileUpload = (event) => {
  uploadedFile.value = event.target.files[0];
};

const isDisabled = computed(
  () => feedbackText.value.trim() === "" && issueDesc.value.trim() === ""
);

const submitFeedback = () => {
  if (!isDisabled.value) {
    console.log("Feedback Submitted:", {
      feedback: feedbackText.value,
      rating: rating.value,
      issueType: issueType.value,
      issueDesc: issueDesc.value,
      priority: priority.value,
      uploadedFile: uploadedFile.value ? uploadedFile.value.name : "No file uploaded",
    });

    submitted.value = true;
    setTimeout(() => {
      submitted.value = false;
      feedbackText.value = "";
      issueType.value = "";
      issueDesc.value = "";
      priority.value = "";
      charCount.value = 0;
      rating.value = 0;
      uploadedFile.value = null;
    }, 3000);
  }
};
</script>

<style scoped>
/* Main Container */
.feedback-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1e1e1e, #121212);
  text-align: center;
  padding: 40px;
  animation: fadeIn 1s ease-in-out;
}

/* Fade In Animation */
@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Glassmorphism Card */
.feedback-content {
  max-width: 500px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease-in-out;
}

.feedback-content:hover {
  transform: scale(1.02);
}

/* Titles */
.feedback-title {
  font-size: 28px;
  font-weight: bold;
  color: #5fefff;
  text-transform: uppercase;
}

.feedback-subtitle {
  font-size: 16px;
  color: #bbb;
  margin-bottom: 20px;
}

/* Rating System */
.rating-container {
  margin-bottom: 15px;
}

.star {
  font-size: 30px;
  color: #444;
  cursor: pointer;
  transition: color 0.3s ease-in-out;
}

.star.active {
  color: #fdbc00;
}

.star:hover {
  color: #ffd700;
}

/* Feedback Form */
.feedback-form {
  display: flex;
  flex-direction: column;
}

.feedback-input {
  width: 100%;
  height: 100px;
  padding: 10px;
  font-size: 16px;
  border-radius: 8px;
  border: none;
  resize: none;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  outline: none;
}

.char-count {
  font-size: 14px;
  color: #ccc;
  text-align: right;
  margin-top: 5px;
}

/* Section Title */
.section-title {
  font-size: 20px;
  color: #5fefff;
  margin-top: 20px;
  text-align: left;
}

/* Dropdown & File Input */
.dropdown,
.file-input {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: none;
  font-size: 16px;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  margin-top: 10px;
}

/* Submit Button */
.submit-btn {
  background: #5fefff;
  color: black;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease-in-out;
  margin-top: 10px;
}

.submit-btn:hover {
  background: #007bff;
  color: white;
}

.submit-btn:disabled {
  background: #444;
  cursor: not-allowed;
}

/* Success Message */
.success-message {
  margin-top: 15px;
  font-size: 16px;
  color: #0f0;
  animation: popIn 0.5s ease-in-out;
}

/* Pop-In Animation */
@keyframes popIn {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
