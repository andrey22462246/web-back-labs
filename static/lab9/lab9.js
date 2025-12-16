document.addEventListener('DOMContentLoaded', function() {
    
    const giftsContainer = document.getElementById('gifts-container');
    const openedCountElement = document.getElementById('opened-count');
    const availableCountElement = document.getElementById('available-count');
    const statusElement = document.getElementById('status');
    const errorMessageElement = document.getElementById('error-message');
    const successMessageElement = document.getElementById('success-message');
    const modal = document.getElementById('congrat-modal');
    
    
    let openedGifts = [];
    let positions = [];
    let openedCount = 0;
    let isAuthenticated = false;
    let username = '';
    let availableCount = 9;
    
    
    initGame();
    
    async function initGame() {
        try {
            const response = await fetch('/lab9/get_state');
            const data = await response.json();
            
            if (data.success) {
                updateStateFromServer(data);
                renderGifts();
            } else {
                showError(data.error);
            }
        } catch (error) {
            showError('Ошибка загрузки');
        }
    }
    
    
    function updateStateFromServer(data) {
        positions = data.positions;
        openedGifts = data.opened_gifts;
        openedCount = data.opened_count;
        availableCount = data.available_count;
        isAuthenticated = data.authenticated;
        username = data.username;
        
        updateStats();
        updateSantaButton();
        updateAuthUI();
    }
    
    
    function updateAuthUI() {
        const loginForm = document.getElementById('login-form');
        const userInfo = document.querySelector('.user-info');
        
        if (loginForm && userInfo) {
            if (isAuthenticated) {
                loginForm.style.display = 'none';
                userInfo.style.display = 'flex';
                const userNameElement = document.querySelector('.user-name');
                if (userNameElement) {
                    userNameElement.textContent = username;
                }
            } else {
                loginForm.style.display = 'flex';
                userInfo.style.display = 'none';
            }
        }
    }
    
    function updateSantaButton() {
        const santaButton = document.querySelector('.btn-santa');
        if (santaButton) {
            santaButton.style.display = isAuthenticated ? 'flex' : 'none';
        }
    }
    
    function renderGifts() {
        giftsContainer.innerHTML = '';
        
        
        const tree = document.createElement('div');
        tree.className = 'tree-decoration';
        tree.innerHTML = `
            <div class="tree">🎄</div>
            <div class="lights">
                <span class="light red"></span>
                <span class="light blue"></span>
                <span class="light green"></span>
                <span class="light yellow"></span>
                <span class="light purple"></span>
            </div>
        `;
        giftsContainer.appendChild(tree);
        
        
        positions.forEach((pos) => {
            const gift = document.createElement('div');
            gift.className = `gift-box ${pos.opened ? 'opened' : ''}`;
            gift.id = `gift-${pos.id}`;
            gift.style.top = pos.top;
            gift.style.left = pos.left;
            gift.dataset.id = pos.id;
            
            
            const giftNumber = pos.id + 1;
            const imgUrl = `/static/lab9/gifts/gift_box${giftNumber}.png`;
            
            
            const isLocked = pos.requires_auth && !isAuthenticated && !pos.opened;
            if (isLocked) {
                gift.classList.add('locked');
            }
            
            if (pos.opened) {
                gift.innerHTML = `<img src="${imgUrl}" alt="Открыт">`;
                gift.style.pointerEvents = 'none';
                gift.style.opacity = '0.6';
            } else {
                gift.innerHTML = `<img src="${imgUrl}" alt="Подарок">`;
                
                if (!isLocked) {
                    gift.addEventListener('click', () => openGift(pos.id));
                    gift.title = 'Нажмите чтобы открыть';
                    gift.style.cursor = 'pointer';
                    gift.style.animation = 'pulse 2s infinite';
                } else {
                    gift.title = 'Особый подарок - требуется вход';
                    gift.style.cursor = 'not-allowed';
                    gift.addEventListener('click', () => {
                        showError('🔒 Этот подарок доступен только для авторизованных пользователей');
                    });
                }
            }
            
            giftsContainer.appendChild(gift);
        });
    }
    
    async function openGift(giftId) {
        if (openedGifts.includes(giftId)) {
            showError('Этот подарок уже открыт!');
            return;
        }
        
        if (openedCount >= 3) {
            showError('Вы уже открыли максимальное количество подарков (3)');
            return;
        }
        
        try {
            const response = await fetch('/lab9/open_gift', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ gift_id: giftId })
            });
            
            const data = await response.json();
            
            if (data.success) {
                openedCount = data.opened_count;
                openedGifts.push(giftId);
                
                
                for (let pos of positions) {
                    if (pos.id === giftId) {
                        pos.opened = true;
                        break;
                    }
                }
                
                updateStats();
                showCongratulation(data.congratulation);
                
                
                const giftElement = document.getElementById(`gift-${giftId}`);
                if (giftElement) {
                    giftElement.classList.add('opened');
                    giftElement.style.pointerEvents = 'none';
                    giftElement.style.opacity = '0.6';
                    giftElement.style.animation = 'none';
                }
            } else {
                showError(data.error);
            }
        } catch (error) {
            showError('Ошибка соединения');
        }
    }
    
    async function login() {
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        const usernameValue = usernameInput.value.trim();
        const passwordValue = passwordInput.value.trim();
        
        if (!usernameValue || !passwordValue) {
            showError('Введите имя пользователя и пароль');
            return;
        }
        
        showLoading('Вход...');
        
        try {
            const response = await fetch('/lab9/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ 
                    username: usernameValue,
                    password: passwordValue 
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showSuccess(data.message);
                
                
                setTimeout(async () => {
                    
                    await initGame();
                }, 300);
                
                
                usernameInput.value = '';
                passwordInput.value = '';
            } else {
                showError(data.error);
            }
        } catch (error) {
            showError('Ошибка входа');
        }
    }
    
    async function logout() {
        try {
            const response = await fetch('/lab9/logout', { method: 'POST' });
            const data = await response.json();
            
            if (data.success) {
                showSuccess(data.message);
                
                
                setTimeout(async () => {
                    await initGame();
                }, 300);
            }
        } catch (error) {
            showError('Ошибка выхода');
        }
    }
    
    async function santaRefill() {
        if (!isAuthenticated) {
            showError('Эта функция доступна только для авторизованных пользователей');
            return;
        }
        
        if (!confirm('🎅 Дед Мороз перемешает все подарки! Открытые подарки сбросятся. Продолжить?')) {
            return;
        }
        
        showLoading('Дед Мороз работает...');
        
        try {
            const response = await fetch('/lab9/santa_refill', { method: 'POST' });
            const data = await response.json();
            
            if (data.success) {
                showSuccess(data.message);
                
                
                setTimeout(async () => {
                    await initGame();
                }, 300);
            } else {
                showError(data.error);
            }
        } catch (error) {
            showError('Ошибка');
        }
    }
    
    function showCongratulation(congrat) {
        document.getElementById('congrat-text').textContent = congrat.text;
        document.getElementById('congrat-gift-name').textContent = congrat.gift_name;
        
        const img = document.getElementById('congrat-gift-image');
        img.src = `/static/lab9/images/${congrat.image}`;
        img.alt = congrat.gift_name;
        
        modal.style.display = 'flex';
        setTimeout(() => modal.classList.add('show'), 10);
    }
    
    function updateStats() {
        openedCountElement.textContent = `${openedCount}/3`;
        availableCountElement.textContent = availableCount;
        
        if (openedCount >= 3) {
            statusElement.textContent = 'Все подарки найдены!';
            statusElement.style.color = 'gold';
        } else if (openedCount > 0) {
            statusElement.textContent = 'Ищем дальше...';
            statusElement.style.color = 'lightgreen';
        } else {
            statusElement.textContent = 'Готов к поиску!';
            statusElement.style.color = 'lightblue';
        }
    }
    
    function showLoading(message = 'Загрузка...') {
        statusElement.textContent = message;
        statusElement.style.color = 'var(--new-year-blue)';
    }
    
    function showError(message) {
        errorMessageElement.textContent = message;
        errorMessageElement.style.display = 'block';
        setTimeout(() => {
            errorMessageElement.style.display = 'none';
        }, 3000);
    }
    
    function showSuccess(message) {
        successMessageElement.textContent = message;
        successMessageElement.style.display = 'block';
        setTimeout(() => {
            successMessageElement.style.display = 'none';
        }, 3000);
    }
    
    
    window.closeModal = function() {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
    };
    
    window.login = login;
    window.logout = logout;
    window.santaRefill = santaRefill;
    
    window.showHelp = function() {
        alert('🎮 Правила игры:\n\n' +
              '1. Найдите и откройте 3 подарка из доступных\n' +
              '2. Без входа доступно 9 подарков (1 заблокирован)\n' +
              '3. Для входа используйте тестовые аккаунты:\n' +
              '   - user / 123\n' +
              '   - admin / admin\n' +
              '   - гость / праздник\n' +
              '4. После входа доступны все 10 подарков\n' +
              '5. Кнопка "Позвать Деда Мороза" доступна ТОЛЬКО авторизованным\n' +
              '6. Позиции подарков случайны и сохраняются в сессии');
    };
    
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });
});