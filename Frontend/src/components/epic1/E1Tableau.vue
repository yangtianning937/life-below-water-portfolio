<template>
  <div class="tableau-container">
    <div
      class="tableauPlaceholder"
      ref="tableauDiv"
      style="position: relative; width: 100%; height: 100%;"
    >
      <noscript>
        <a href="#">
          <img
            alt="Tableau Static"
            :src="staticImage"
            style="border: none"
          />
        </a>
      </noscript>
      <object class="tableauViz" style="display:none;">
        <param name="host_url" value="https%3A%2F%2Fpublic.tableau.com%2F" />
        <param name="embed_code_version" value="3" />
        <param name="site_root" value="" />
        <param name="name" :value="workbook + '/' + sheet" />
        <param name="tabs" :value="tabs ? 'yes' : 'no'" />
        <param name="toolbar" :value="toolbar ? 'yes' : 'no'" />
        <param name="static_image" :value="staticImage" />
        <param name="animate_transition" value="yes" />
        <param name="display_static_image" value="yes" />
        <param name="display_spinner" value="yes" />
        <param name="display_overlay" value="yes" />
        <param name="display_count" value="yes" />
        <param name="language" value="en-US" />
      </object>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

const props = defineProps({
  workbook: { type: String, required: true }, // e.g. "NewWorkbook_17569007097240"
  sheet: { type: String, required: true },    // e.g. "Sheet1"
  staticImage: { type: String, required: true }, // Tableau 提供的静态图 URL
  tabs: { type: Boolean, default: false },
  toolbar: { type: Boolean, default: true },
});

const tableauDiv = ref(null);

onMounted(() => {
  const vizElement = tableauDiv.value.getElementsByTagName("object")[0];
  vizElement.style.width = "100%";
  vizElement.style.height = tableauDiv.value.offsetWidth * 0.75 + "px";

  const scriptElement = document.createElement("script");
  scriptElement.src = "https://public.tableau.com/javascripts/api/viz_v1.js";
  vizElement.parentNode.insertBefore(scriptElement, vizElement);
});
</script>

<style scoped>
.tableau-container {
  width: 100%;
  height: 100%;
  min-height: 520px;
}
</style>
