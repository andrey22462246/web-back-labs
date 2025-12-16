document.addEventListener('DOMContentLoaded', function() {
    // Элементы DOM
    const giftsContainer = document.getElementById('gifts-container');
    const openedCountElement = document.getElementById('opened-count');
    const remainingCountElement = document.getElementById('remaining-count');
    const statusElement = document.getElementById('status');
    const errorMessageElement = document.getElementById('error-message');
    const modal = document.getElementById('congrat-modal');
    
    // Состояние игры
    let openedGifts = [];
    let positions = [];
    let openedCount = 0;
    
    // Инициализация игры
    initGame();
    
    // Функция инициализации игры
    async function initGame() {
        showLoading();
        
        try {
            const response = await fetch('/lab9/get_state');
            const data = await response.json();
            
            if (data.success) {
                positions = data.positions;
                openedGifts = data.opened_gifts;
                openedCount = data.opened_count;
                
                updateStats();
                renderGifts();
            } else {
                showError(data.error || 'Ошибка загрузки состояния игры');
            }
        } catch (error) {
            showError('Ошибка соединения с сервером');
        }
    }
    
    // Функция рендеринга подарков
    function renderGifts() {
        giftsContainer.innerHTML = '';
        
        // Добавляем ёлку
        const treeDecoration = document.createElement('div');
        treeDecoration.className = 'tree-decoration';
        treeDecoration.innerHTML = `
            <div class="tree">🎄</div>
            <div class="lights">
                <span class="light red"></span>
                <span class="light blue"></span>
                <span class="light green"></span>
                <span class="light yellow"></span>
                <span class="light purple"></span>
            </div>
        `;
        giftsContainer.appendChild(treeDecoration);
        
        // Добавляем подарки
        positions.forEach((pos) => {
            const gift = document.createElement('div');
            gift.className = `gift-box ${pos.opened ? 'opened' : ''}`;
            gift.id = `gift-${pos.id}`;
            gift.style.top = pos.top;
            gift.style.left = pos.left;
            gift.dataset.id = pos.id;
            
            // Используем картинку из позиции
            const boxImage = pos.box_image || `/static/lab9/gifts/gift_box${(pos.id % 10) + 1}.png`;
            
            if (pos.opened) {
                gift.innerHTML = `
                    <img src="${boxImage}" alt="Подарок (открыт)">
                `;
                gift.style.pointerEvents = 'none';
                gift.style.opacity = '0.5';
                gift.title = 'Подарок уже открыт';
            } else {
                gift.innerHTML = `
                    <img src="${boxImage}" alt="Подарок">
                `;
                gift.addEventListener('click', () => openGift(pos.id));
                gift.title = 'Нажмите, чтобы открыть подарок';
                
                // Добавляем анимацию пульсации для неоткрытых подарков
                gift.style.animation = `pulse 2s infinite`;
            }
            
            // Добавляем анимацию появления
            gift.style.animationDelay = `${pos.id * 0.1}s`;
            giftsContainer.appendChild(gift);
        });
    }
    
    // Функция открытия подарка
    async function openGift(giftId) {
        if (openedGifts.includes(giftId)) {
            showError('Этот подарок уже открыт!');
            return;
        }
        
        if (openedCount >= 3) {
            showError('Вы уже открыли максимальное количество подарков (3)');
            return;
        }
        
        showLoading('Открываем подарок...');
        
        try {
            const response = await fetch('/lab9/open_gift', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ gift_id: giftId })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Обновляем состояние
                openedCount = data.opened_count;
                openedGifts.push(giftId);
                
                // Обновляем статистику
                updateStats();
                
                // Показываем поздравление
                showCongratulation(data.congratulation);
                
                // Обновляем отображение подарка
                const giftElement = document.getElementById(`gift-${giftId}`);
                if (giftElement) {
                    // Добавляем анимацию открытия
                    giftElement.style.animation = 'openGift 0.5s forwards';
                    
                    setTimeout(() => {
                        giftElement.classList.add('opened');
                        giftElement.style.pointerEvents = 'none';
                        giftElement.style.animation = 'none';
                        giftElement.title = 'Подарок уже открыт';
                    }, 500);
                }
            } else {
                if (data.limit_reached) {
                    showError(data.error, true);
                } else {
                    showError(data.error);
                }
            }
        } catch (error) {
            showError('Ошибка соединения с сервером');
        }
    }
    
    // Функция показа поздравления - используем image из congrat
    function showCongratulation(congrat) {
        // Устанавливаем данные в модальное окно
        document.getElementById('congrat-text').textContent = congrat.text;
        document.getElementById('congrat-gift-name').textContent = congrat.gift_name;
        
        // Устанавливаем картинку подарка ИЗ ПОЗДРАВЛЕНИЯ
        const giftImage = document.getElementById('congrat-gift-image');
        giftImage.src = `/static/lab9/images/${congrat.image}`;  // Важно: берем из congrat
        giftImage.alt = congrat.gift_name;
        giftImage.style.display = 'block';
        
        // Показываем модальное окно
        modal.style.display = 'flex';
        
        setTimeout(() => {
            modal.classList.add('show');
        }, 10);
    }
    
    // Функция обновления статистики
    function updateStats() {
        openedCountElement.textContent = `${openedCount}/3`;
        remainingCountElement.textContent = 10 - openedGifts.length;
        
        // Обновляем статус
        if (openedCount >= 3) {
            statusElement.textContent = 'Все подарки найдены!';
            statusElement.style.color = 'var(--new-year-gold)';
        } else if (openedCount > 0) {
            statusElement.textContent = 'Ищем дальше...';
            statusElement.style.color = 'var(--new-year-green)';
        } else {
            statusElement.textContent = 'Готов к поиску!';
            statusElement.style.color = 'var(--new-year-blue)';
        }
    }
    
    // Функция показа ошибки
    function showError(message, isWarning = false) {
        errorMessageElement.textContent = message;
        errorMessageElement.className = `error-message ${isWarning ? 'warning' : ''}`;
        errorMessageElement.style.display = 'block';
        
        setTimeout(() => {
            errorMessageElement.style.display = 'none';
        }, 3000);
    }
    
    // Функция показа загрузки
    function showLoading(message = 'Загрузка...') {
        statusElement.textContent = message;
        statusElement.style.color = 'var(--new-year-blue)';
    }
    
    // Глобальные функции для кнопок
    window.closeModal = function() {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
    };
    
    window.resetGame = async function() {
        if (!confirm('Вы уверены, что хотите начать заново? Все открытые подарки будут сброшены.')) {
            return;
        }
        
        showLoading('Сброс игры...');
        
        try {
            const response = await fetch('/lab9/reset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Сбрасываем состояние
                openedCount = 0;
                openedGifts = [];
                
                // Перезагружаем состояние игры
                await initGame();
                
                // Показываем сообщение об успехе
                showError('Игра сброшена!', true);
            } else {
                showError(data.error);
            }
        } catch (error) {
            showError('Ошибка соединения с сервером');
        }
    };
    
    window.showHelp = function() {
        alert('🎮 Правила игры:\n\n' +
              '1. Найдите и откройте 3 подарка из 10\n' +
              '2. Каждый подарок содержит уникальное поздравление\n' +
              '3. Позиции подарков сохраняются в вашей сессии\n' +
              '4. Обновите страницу или нажмите "Начать заново", чтобы изменить позиции\n' +
              '5. Открытые подарки помечаются и больше не могут быть открыты');
    };
    
    // Обработчик закрытия модального окна по клику на фон
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            window.closeModal();
        }
    });
});