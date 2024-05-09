let data = [];

function sortTable(columnIndex) {
    let dataType = null
    if (columnIndex == 0) {
        dataType = typeof data[0].pk;
    }
    if (columnIndex == 1) {
        dataType = typeof data[0].fields.cpu_utilization;
    }
    data.sort((a, b) => {
        if (columnIndex == 0) {
            return a.pk - b.pk;
        } else {
            return a.fields.cpu_utilization - b.fields.cpu_utilization;
        }
        });
    updateTable();
}

function fetchData() {
  const xhr = new XMLHttpRequest();
  xhr.open('GET', '/ajax_ep/', true);
  xhr.onload = function() {
    if (xhr.status === 200) {
      // Успешное получение данных
      data = JSON.parse(xhr.responseText);
      updateTable();
    } else {
      // Ошибка при получении данных
      console.error('Ошибка при получении данных:', xhr.statusText);
    }
  };
  xhr.onerror = function() {
    console.error('Ошибка сети');
  };
  xhr.send();
}

function updateTable() {
  const tableBody = document.querySelector('#data-table tbody');
  tableBody.innerHTML = ''; // Очистка содержимого таблицы
  data.forEach(item => {
    const row = document.createElement('tr');

    // Создание ячеек таблицы для каждого свойства объекта
    const cell_pk = document.createElement('td');
    cell_pk.textContent = item.pk;
    row.appendChild(cell_pk);
    const cell = document.createElement('td');
    cell.textContent = item.fields.cpu_utilization;
    row.appendChild(cell);

    tableBody.appendChild(row);
  });
  calculateAggregateData();
}

// Функция для вычисления агрегированных данных
function calculateAggregateData() {
    const values = data.map((row) => row.fields.cpu_utilization);
    const minValue = Math.min(...values);
    const maxValue = Math.max(...values);
    const avgValue = values.reduce((acc, curr) => acc + curr, 0) / values.length;
    document.getElementById('min-value').textContent = minValue;
    document.getElementById('max-value').textContent = maxValue;
    document.getElementById('avg-value').textContent = avgValue.toFixed(2);
}

fetchData(); // Первоначальная загрузка данных
setInterval(fetchData, 10000); // Обновление данных каждые 10 секунд