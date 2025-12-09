document.addEventListener('DOMContentLoaded', function() {
    console.log('🎄 Новогодние подарки загружены!');
    
    // Загружаем подарки при загрузке страницы
    loadGifts();
    
    // Создаём снежинки
    createSnowflakes();
    
    // Назначаем обработчики событий
    setupEventListeners();
});


async function loadGifts() {
    try {
        showLoading(true);
        
        const response = await fetch('/lab9/api/gifts');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            updateUI(data);
            renderGifts(data.gifts);
        } else {
            showError('Ошибка загрузки данных');
        }
    } catch (error) {
        console.error('Ошибка загрузки подарков:', error);
        showError('Не удалось загрузить подарки. Попробуйте обновить страницу.');
    } finally {
        showLoading(false);
    }
}

/**
 * Открытие подарка
 * @param {number} giftId - ID подарка
 */
async function openGift(giftId) {
    try {
        showLoading(true);
        
        const response = await fetch(`/lab9/api/open/${giftId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showCongratulations(data);
            loadGifts(); // Обновляем UI
        } else {
            showError(data.message);
        }
    } catch (error) {
        console.error('Ошибка при открытии подарка:', error);
        showError('Ошибка сети. Проверьте подключение.');
    } finally {
        showLoading(false);
    }
}

/**
 * Показать поздравление в модальном окне
 * @param {Object} data - Данные о подарке
 */
function showCongratulations(data) {
    const modal = document.getElementById('congrat-modal');
    const giftImage = document.getElementById('congrat-gift-image');
    const giftName = document.getElementById('congrat-gift-name');
    const congratText = document.getElementById('congrat-text');
    
    // Устанавливаем данные
    giftImage.src = data.gift_image;
    giftImage.alt = data.gift_name;
    giftName.textContent = data.gift_name;
    congratText.textContent = data.congratulation;
    
    // Показываем модальное окно с анимацией
    modal.style.display = 'flex';
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
    
    // Добавляем праздничный эффект
    createConfetti();
}

/**
 * Закрыть модальное окно
 */
function closeModal() {
    const modal = document.getElementById('congrat-modal');
    modal.classList.remove('show');
    
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
}

/**
 * Обновление интерфейса
 * @param {Object} data - Данные с сервера
 */
function updateUI(data) {
    // Обновляем счётчики
    const openedCount = document.getElementById('opened-count');
    const remainingCount = document.getElementById('remaining-count');
    const statusElement = document.getElementById('status');
    
    if (openedCount) {
        openedCount.textContent = `${data.opened_count}/${data.max_opens}`;
    }
    
    if (remainingCount) {
        remainingCount.textContent = data.remaining;
    }
}