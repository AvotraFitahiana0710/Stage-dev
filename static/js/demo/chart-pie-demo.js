// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';


const totalAccounts = parseInt(document.getElementById('total-accounts').textContent.match(/\d+/)[0]);
const adminCount = parseInt(document.getElementById('admin-count').textContent.match(/\d+/)[0]);
const managerCount = parseInt(document.getElementById('manager-count').textContent.match(/\d+/)[0]);
const employeeCount = parseInt(document.getElementById('employee-count').textContent.match(/\d+/)[0]);

// Calculer les pourcentages
const adminPercentage = ((adminCount / totalAccounts) * 100).toFixed(2);
const managerPercentage = ((managerCount / totalAccounts) * 100).toFixed(2);
const employeePercentage = ((employeeCount / totalAccounts) * 100).toFixed(2);

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Administrateurs", "Managers", "Employés"],
    datasets: [{
      data: [adminPercentage, managerPercentage, employeePercentage],
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
