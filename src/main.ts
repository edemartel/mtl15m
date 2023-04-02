import { createApp } from 'vue';

import './assets/style.css';
import 'vue-select/dist/vue-select.css';
import '@fortawesome/fontawesome-free/css/fontawesome.css';
import '@fortawesome/fontawesome-free/css/solid.css';

import App from './App.vue';
import { createPinia } from 'pinia';
import { createI18n } from 'vue-i18n';

import frCA from './locales/fr-CA';
import enCA from './locales/en-CA';

const app = createApp(App);

const pinia = createPinia();
app.use(pinia);

const i18n = createI18n({
    legacy: false,
    globalInjection: true,
    warnHtmlMessage: false,  // used for tutorial per-word styling
    locale: 'fr-CA',
    messages: {
        'fr-CA': frCA,
        'en-CA': enCA
    }
});
app.use(i18n);

app.mount('#app');
