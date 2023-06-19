<template>
  <canvas :id="`myChart${id}`"></canvas>
</template>

<script>
import Chart from 'chart.js/auto';
export default {
  name: 'AnalysisBarChart',
  props: {
    id: { type: String, required: true },
    ['labels']: { type: String, required: true },
    ['values']: { type: String, required: true },
    ['no_completed']: { type: String, required: true },
    ['no_crossed']: { type: String, required: true },
  },
  mounted() {
    const ctx = document.getElementById('myChart' + this.id).getContext('2d');
    const myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: this.labels.split(','),
        datasets: [
          {
            label: '# of Tasks',
            data: this.values.split(','),
            backgroundColor: ['rgba(0, 0, 0, 0.2)'],
            borderColor: ['rgba(0, 0, 0, 1)'],
            borderWidth: this.id,
            options: {
              animation: {
                bar: {
                  delay: 1000,
                  easing: 'linear',
                },
              },
            },
          },
          {
            label: '# of Completed Tasks',
            data: this.no_completed.split(','),
            backgroundColor: 'rgba(0, 252, 0, 0.2)',
            borderColor: 'rgba(0, 252, 0, 1)',
            borderWidth: 1,
            options: {
              animation: {
                bar: {
                  delay: 1000,
                  easing: 'linear',
                },
              },
            },
          },
          {
            label: '# of Tasks that has crossed the Deadline',
            data: this.no_crossed.split(','),
            backgroundColor: 'rgba(252, 0, 0, 0.2)',
            borderColor: 'rgba(252, 0, 0, 1)',
            borderWidth: 1,
            options: {
              animation: {
                bar: {
                  delay: 1000,
                  easing: 'linear',
                },
              },
            },
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
    myChart;
  },
};
</script>

<style></style>
