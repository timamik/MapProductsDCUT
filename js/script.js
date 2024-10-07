var map = L.map('map', {
    attributionControl: false
}).setView([55.751244, 37.618423], 10); // Координаты центра Москвы и уровень масштабирования 11


// Добавляем тайлы карты
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

// Функция для расчета размера маркера на основе description2
function calculateSize(description2, minVal, maxVal) {
    return 5 + ((description2 - minVal) / (maxVal - minVal)) * 25;
}

// Функция для расчета цвета на основе description2
function calculateColor(description2, minVal, maxVal) {
    var intensity = (description2 - minVal) / (maxVal - minVal);
    var red = Math.floor(255 * intensity);
    return `rgb(${red}, 100, 150)`;
}

// Загружаем JSON с данными
fetch('data/updated_data.json')
    .then(response => response.json())
    .then(data => {
        var minDescription2 = Math.min(...data.flatMap(org => org.locations.map(loc => parseFloat(loc.description2))));
        var maxDescription2 = Math.max(...data.flatMap(org => org.locations.map(loc => parseFloat(loc.description2))));

        // Добавляем маркеры на карту
        data.forEach(function(org) {
            org.locations.forEach(function(loc) {
                var description2 = parseFloat(loc.description2);
                var size = calculateSize(description2, minDescription2, maxDescription2);
                var color = calculateColor(description2, minDescription2, maxDescription2);

                // Добавляем маркер с динамическим стилем
                var marker = L.circleMarker([loc.latitude, loc.longitude], {
                    radius: size,
                    color: color,
                    fillColor: color,
                    fillOpacity: 0.5,
                    weight: 2,
                    opacity: 1,
                    dashArray: '3',
                    dashOffset: '0'
                }).addTo(map)
                    .bindPopup(`<a href="http://https://timamik.github.io/MapProductsDCUT/table.html?id=${encodeURIComponent(org.name)}" target="_blank"><b>${org.name}</b></a><br>${loc.description1}: шт. <br>${description2.toLocaleString('ru-RU', { style: 'currency', currency :'RUB'})}<br>${loc.address}</br>`);

            });
        });
    })
    .catch(error => {
        console.error('Ошибка при загрузке JSON:', error);
    });
