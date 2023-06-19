<template>
  <div class="delete__list"></div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';
export default {
  name: 'deleteTask',
  mounted() {
    const router = useRouter();
    axios
      .delete('http://localhost:5000/deleteTask/' + this.$route.params.tid)
      .then((res) => {
        console.log(res);
        alert('Your Task was Successfully deleted');
        router.push({ name: 'Dashboard', params: { id: localStorage['id'] } });
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>

<style></style>
