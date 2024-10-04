// Инициализируем карту
var map = L.map('map', {
    attributionControl: false  // Отключаем атрибуцию
}).setView([55.751244, 37.618423], 10);

// Добавляем тайлы карты
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

// Добавляем маркер с popup и измененными размерами окна
var circle = L.circle([55.751244, 37.618423], {
    color: 'blue',      // Цвет контура
    fillColor: '#30f',  // Цвет заливки
    fillOpacity: 0.5,   // Прозрачность заливки
    radius: 10         // Радиус круга в метрах
}).addTo(map);

// Создаем круг с небольшим радиусом
circle.bindTooltip("Это круг", {
    permanent: true,   // Метка всегда видима
    direction: 'top',  // Позиция метки - сверху маркера
    offset: [0, 0]   // Отступ для лучшего позиционирования
}).openTooltip();
/*
marker.bindPopup("<b>232323</b>", {
    maxWidth: 300,  // Устанавливаем максимальную ширину через Leaflet
    minWidth: 200,  // Минимальная ширина окна
    maxHeight: 200  // Максимальная высота
}).openPopup();
*/