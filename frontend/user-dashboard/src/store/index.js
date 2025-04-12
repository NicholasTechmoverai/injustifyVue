import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    email: 'injustify@gamil.com',
    name: 'injustify',
    vShowNavbar:true,
    SnackBar_messages:[],
  }),
  actions: {
    setShowNavbar(s){
      this.vShowNavbar = s;
    },
    setUser(data) {
      this.email = data.email;
      this.userId = data.id; 
      this.name = data.name;
      this.profilePic = data.picture; 
      this.verifiedEmail = data.verified_email;
      this.created_at = data.created_at;
    
      //store the login user in cookie for 3days
      const dataWithExpiry = {
        ...data,
        expiresAt: Date.now() + 3 * 24 * 60 * 60 * 1000
      };
      
      const jsonString = encodeURIComponent(JSON.stringify(dataWithExpiry));
      const expires = new Date(dataWithExpiry.expiresAt).toUTCString();
      
      document.cookie = `user_info=${jsonString}; expires=${expires}; path=/`;
      
    },
    
    clearUser() {
      this.email = '';
      this.name = '';
      this.profilePic = '';
      this.verifiedEmail = false;
      this.userId = null;
      this.created_at  = '';
    },
    setActivePlaylist(playlistId){
      this.activePlaylistId = playlistId;
    },

    //handle playlist, add song, remove song, etc. methods here
    setPlaylistSongs(songs,playlistName) {
      this.songs =null || [songs]; 
      this.playlistName = playlistName;
    
    },
    
    setMainContainerWidthMarginLeft(val){
      this.iscollapsedBig = val;
    },
    //set theme
    setTheme(val) {
      this.isdarkmode = val;
      document.cookie = `isDarkmode=${val}`
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

    },
    set_snackbarMessage(message, type = "info", tm = 10000) {
      const id = Date.now();
      this.SnackBar_messages.push({ id, message, type });
    
      setTimeout(() => {
        this.delete_snackBarMessage(id);        
      }, tm);
    },
    
    delete_snackBarMessage(id) {
      this.SnackBar_messages = this.SnackBar_messages.filter(msg => msg.id !== id);
    }
    

  }
});

