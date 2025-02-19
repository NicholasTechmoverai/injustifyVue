<template>
  <div v-if="loading" id="loading">
    <ion-icon name="reload-outline"></ion-icon>
  </div>
  <div id="profileUserInfo">
    <div id="profile-pic">
      <div class="profile-pic-ON">
        <img 
          :src="user.picture || defaultProfilePic" 
          alt="Profile Picture" 
          class="circular-profile_pic" 
          @click="triggerFileInput"
        />
      </div>
      <div class="profile-edit">
        <button type="button" id="saveprofileChanges" @click="saveProfileChanges">
          <i class="fas fa-pencil-alt"></i> Save
        </button>
      </div>
    </div>

    <div class="profile-info">
      <h3>{{ user.name }}</h3>
      <p v-if="user.created_at">User since: {{ formattedDate }}</p>

      <div id="userEmail" class="card" :class="themeClass">
        <div id="veryEmail">{{ user.email }}</div>
        <div v-if="user.verified_email === 1" id="verifiedState">
          <i class="fas fa-check-circle"></i>
          <span>Verified</span>
        </div>
      </div>

      <div id="top-songs-Adhered">
        <div id="top-songs-adheredHeader">
          <h3>Top Songs Adhered</h3>
        </div>
        <div class="top-songs-list">
          <div class="artist-socialist">
            <div class="artist-info">
              <img src="" />
              <p>Adele</p>
              <div class="WheatherVerified">
                <i class="fas fa-check-circle"></i>
              </div>
            </div>
            <div class="thesong">
              <h4>Easy On Me</h4>
              <div class="moreOn-song">
                <div class="songPviews">1.5B views</div>
                <div class="songpYear">6 months ago</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Hidden File Input -->
    <input type="file" ref="fileInput" accept="image/*" @change="handleFileChange" style="display: none" />
  </div>
</template>

<script>
import axios from "axios";
import { ref, computed, onMounted } from "vue";

export default {
  name: "UserProfile",
  props: {
    useremail: String,
  },
  setup(props) {
    const user = ref({});
    const newProfilePicture = ref(null);
    const defaultProfilePic = "/path/to/default.jpg";
    const fileInput = ref(null);
    const loading = ref(false); // Fix: Define loading using ref()

    // Theme handling
    const themeClass = computed(() => {
      return document.cookie.includes("theme=dark") ? "dark-mode" : "";
    });

    // Format the date safely
    const formattedDate = computed(() => {
      if (!user.value.created_at) return "Unknown";
      return user.value.created_at.split(" ").slice(1, 4).join(" ");
    });

    // Fetch user profile
    const fetchUserProfile = async () => {
      loading.value = true; // Fix: Use ref() correctly
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/profile/${props.useremail}`);
        user.value = response.data;
      } catch (error) {
        console.error("Error fetching profile:", error);
      } finally {
        loading.value = false; // Fix: Ensure loading is reset
      }
    };

    // Trigger file input when profile picture is clicked
    const triggerFileInput = () => {
      fileInput.value.click();
    };

    // Handle profile picture change
    const handleFileChange = (event) => {
      const file = event.target.files[0];
      if (file) {
        user.value.picture = URL.createObjectURL(file);
        newProfilePicture.value = file;
      }
    };

    // Save profile changes
    const saveProfileChanges = async () => {
      if (!newProfilePicture.value) return;

      const formData = new FormData();
      formData.append("profile_picture", newProfilePicture.value);
      formData.append("user_id", props.userId);

      try {
        await axios.post("http://127.0.0.1:5000/api/update-profile", formData);
        console.log("Profile updated successfully!");
      } catch (error) {
        console.error("Error updating profile:", error);
      }
    };

    onMounted(fetchUserProfile);

    return {
      user,
      loading, // Fix: Ensure loading is returned
      formattedDate,
      themeClass,
      defaultProfilePic,
      fileInput,
      triggerFileInput,
      handleFileChange,
      saveProfileChanges,
    };
  },
};
</script>

<style scoped>
h3 {
  color: #34495e;
}
p {
  font-size: 16px;
  margin: 5px 0;
}
#profile-pic{
    display: flex;
    position: relative;
    width: 100%;
    margin-bottom: 10px;
    align-items: center;
    justify-content: center;
}
.profile-pic-ON{
    width: 100px !important;
    height: 100px !important;
    background-color: #646060;
    border-radius: 50%;

}
.profile-pic-ON img{
    width: 100%;
    height: 100%;
}
#settings .dropdown .dropdown-content a{
    color: inherit;
    padding: 8px 16px;
    text-decoration: none;
    display: block;
    transition: background-color 0.3s ease;
}
#settings .dropdown .dropdown-content a:hover{
    background-color: #6b6a6a20;
}
#profileUserInfo{
    margin: 0 auto;
    display:flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
}
.profile-info{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1px;
    position: relative;
}

 .profile-edit{
    position: absolute;
    top: 90%;
    right: 10px;
}
 .artist-socialist{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    gap: 15px;
}
#profile{
    display: none;
    flex-direction: column;
}
.artist-info{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1px;
    position: relative;
}

.artist-info img{
    width: 30px;
    height: 30px;
    border-radius: 50%;
    object-fit: cover;
}
.moreOn-song{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    font-size: 12px;
}
 .WheatherVerified{
    position: absolute;
    top: 10%;
    right: 0;
}

#top-songs-Adhered{
    margin-top: 30px;
}

#top-songs-adheredHeader{
    padding:3px;
}

 #top-songs-list{
    display: flex;
    flex-direction: row;
    gap: 10px;
}
 #userEmail{
    display: flex;
    flex-direction: row;
    gap: 10px;
    padding: 5px;
}

 #verifiedState{
    color:green;
}



</style>
