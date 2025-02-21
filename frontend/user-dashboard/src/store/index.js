import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    email: 'injustify@gamil.com',
    name: 'injustify'
  }),
  actions: {
    setUser(data) {
      this.email = data.email;
      this.userId = data.id; 
      this.name = data.name;
      this.profilePic = data.picture; 
      this.verifiedEmail = data.verified_email;
      //console.log(this.email, this.name,this.profilePic,this.verifiedEmail,this.userId);  // Log after the state is set
    },
    clearUser() {
      this.email = '';
      this.name = '';
      this.profilePic = '';
      this.verifiedEmail = false;
      this.userId = null;
    },
    setActivePlaylist(playlistId){
      this.activePlaylistId = playlistId;
    }

  }
});

//get cookie with user email and name

const cookieName = 'user_info';
const cookie = document.cookie.split('; ').find(c => c.trim().startsWith(`${cookieName}=`));

if (cookie) {
  const cookieData = JSON.parse(atob(cookie.split('=')[1]));
  useUserStore().setUser(cookieData);
}