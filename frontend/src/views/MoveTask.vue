<template>
  <div class="app"></div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';
export default {
  name: 'MoveTask',
  data() {
    return {
      tid: '',
      lid: '',
    };
  },
  mounted() {
    const router = useRouter();
    const token = localStorage['access_token'];
    this.tid = this.$route.params.tid;
    this.lid = this.$route.params.lid;
    axios
      .post('http://localhost:5000/moveTask/' + this.tid + '/' + this.lid, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((resp) => {
        console.log(resp);
        alert('Your list has been Moved!!');
        router.push({ name: 'Dashboard', params: { id: localStorage['id'] } });
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>

<style></style>
