<template>
  <div class="delete__list"></div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';
export default {
  name: 'deleteList',
  mounted() {
    const router = useRouter();
    axios
      .delete('http://localhost:5000/deleteList/' + this.$route.params.lid)
      .then((res) => {
        console.log(res);
        alert('Your List was Successfully deleted');
        router.push({ name: 'Dashboard', params: { id: localStorage['id'] } });
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>

<style></style>
