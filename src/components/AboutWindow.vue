<!-- eslint-disable vue/no-v-html -->
<template>
  <div>
    <a
      :title="$t('about')"
      :aria-label="$t('about')"
      href="#"
      @click="openModal"
    ><i class="fa-solid fa-circle-question"></i></a>
    <div
      id="modal-container"
      :style="{ display: opened ? 'block' : 'none' }"
      @click="closeModal"
    >
      <div id="modal-wrapper">
        <div
          id="modal"
          @click="ev => ev.stopPropagation()"
        >
          <div id="modal-header">
            <h1
              id="header"
              v-t="'about'"
            ></h1>
            <a
              id="close-button"
              role="button"
              :aria-label="$t('close')"
              @click="closeModal"
            >
              &#10006;
            </a>
          </div>
          <div id="modal-content">
            <div id="body-container">
              <div
                id="body-content"
                v-html="body"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

import { defineComponent, reactive, ref } from 'vue';
import { marked, Renderer } from 'marked';
import axios from 'axios';
import { useI18n } from 'vue-i18n';

const renderer = new Renderer();
renderer.link = function (href: string | null, title: string | null, text: string) {
    const link = marked.Renderer.prototype.link.apply(this, [href, title, text]);
    return link.replace('<a', '<a target="_blank"');
};

export default defineComponent({
    setup() {
        const texts = reactive({
            'fr-CA': '',
            'en-CA': ''
        });
        const opened = ref(false);
        const i18n = useI18n();
        return { opened, texts, i18n };
    },
    computed: {
        body() {
            const locale = this.i18n.locale.value;
            if(locale == 'fr-CA' || locale == 'en-CA') {
                return this.texts[locale];
            }
            return '';
        }
    },
    mounted() {
        const getText = async (locale: string) => {
            const response = await axios.get<string>(`about/${locale}.md`);
            return marked(response.data, { breaks: true, renderer });
        };
        getText('fr-CA').then(x => this.texts['fr-CA'] = x);
        getText('en-CA').then(x => this.texts['en-CA'] = x);
    },
    methods: {
        openModal(ev: Event) {
            this.opened = true;
            ev.preventDefault();
        },
        closeModal(ev: Event) {
            this.opened = false;
            ev.preventDefault();
        }
    }
});
</script>
<style scoped>
#modal-container {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 10000;
}

#modal-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}

#modal {
    max-width: 75%;
    background-color: var(--color-background);
    overflow: hidden;
    border-radius: var(--border-radius);
    box-shadow: 0 3px var(--sz-30) rgba(0, 0, 0, 0.4);
    max-height: 90%;
    display: flex;
    flex-direction: column;
}

@media only screen and (min-width: 600px) {
    #modal {
        max-width: 50%;
    }
}

#close-button {
    cursor: pointer;
    padding: var(--sz-300);
}

#close-button img {
    object-fit: cover;
    width: 100%;
    height: 100%;
}

#close-button:hover {
    opacity: 0.8;
}

#modal-header {
    padding: calc(var(--border-radius) / 4) calc(var(--border-radius) / 4) calc(var(--border-radius) / 4) var(--sz-200);
    background-color: var(--color-background-accent);
    height: var(--sz-900);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

#header {
    font-size: var(--sz-600);
    margin: 0;
}

#modal-content {
    padding-right: var(--sz-300);
    padding-right: var(--sz-300);
    overflow-y: auto;
    overflow-x: hidden;
}

#body-container {
    padding-top: var(--sz-30);
    height: calc(100% - var(--sz-900));
    overflow: hidden;
    border-radius: var(--border-radius);
}

#body-content {
    padding-bottom: var(--sz-50);
    padding-left: var(--sz-100);
    padding-right: var(--sz-100);
    line-height: 1.5em;
    color: var(--clr-gris-moyen);
    font-size: var(--sz-100);
    
    overflow-y: auto;
    overflow-x: hidden;
    height: 100%;
}

#body-content :deep(p) {
    margin: 0;
    margin-bottom: var(--sz-30);
}

#body-content :deep(p):last-child {
    margin-bottom: 0;
}
#body-content :deep(a) {
    color: var(--color-accent);
}

#body-content :deep(a:hover) {
    color: var(--color-text-dark);
}

#body-content :deep(strong) {
    font-weight: var(--fw-regular);
    color: var(--color-text-dark);
}

#body-content :deep(h1) {
    font-size: var(--sz-200);
}

#body-content :deep(ul) {
    padding: 0;
    padding-left: var(--sz-300);;
}
</style>

