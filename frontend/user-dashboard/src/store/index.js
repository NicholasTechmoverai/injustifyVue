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
    },

    //handle playlist, add song, remove song, etc. methods here
    setPlaylistSongs(songs) {
      this.songs =null || [songs]; 
    
    },
    
    setMainContainerWidthMarginLeft(val){
      this.iscollapsedBig = val;
    },
    //set theme
    setTheme(val) {
      this.isdarkmode = val;
    },
    //set the state of any song that is about to download
    set_isAboutToDownload(val) {
      this.isAboutToDownload = val;
    },
    set_streamloading(val) {
      this.streamloading = val;
    },
    set_DownloadFileCredential(info){
      this.downloadFileCredential = info;
      console.log(this.downloadFileCredential);

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