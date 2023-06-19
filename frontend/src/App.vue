<template>
  <div class="app">
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',

  data: () => ({
    //
  }),
};
</script>

<style>
.app {
  width: 100%;
  height: 100%;
}
html,
body {
  height: 100%;
  min-height: 100%;
}
:root {
  --color-bg: #1f1f38;
  --color-bg-variant: #2c2c6c;
  --color-primary: #4db5ff;
  --color-primary-variant: rgba(77, 181, 255, 0.4);
  --color-white: #fff;
  --color-light: rgba(255, 255, 255, 0.6);

  --transition: all 400ms ease;

  --container-width-lg: 75%;
  --container-width-md: 86%;
  --container-width-sm: 90%;
}
</style>
