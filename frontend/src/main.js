import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import store from './store';
import vuetify from './plugins/vuetify';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { loadFonts } from './plugins/webfontloader';
import Datepicker from 'vue3-datepicker';

library.add(fas);

loadFonts();

createApp(App)
  .component('fa', FontAwesomeIcon)
  .component('dp', Datepicker)
  .use(router)
  .use(store)
  .use(vuetify)
  .mount('#app');
