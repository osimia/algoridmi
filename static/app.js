// API Configuration
const API_BASE_URL = window.location.origin;
const API_ENDPOINTS = {
    csrf: `${API_BASE_URL}/api/auth/csrf/`,
    register: `${API_BASE_URL}/api/auth/register/`,
    login: `${API_BASE_URL}/api/auth/login/`,
    logout: `${API_BASE_URL}/api/auth/logout/`,
    profile: `${API_BASE_URL}/api/user/profile/`,
    progress: `${API_BASE_URL}/api/user/progress/`,
    // Gemini AI endpoints (основные)
    generateProblemAI: `${API_BASE_URL}/api/problems/generate-ai/`,
    submitAnswerAI: `${API_BASE_URL}/api/problems/submit-ai/`,
    topicsAI: `${API_BASE_URL}/api/problems/topics-ai/`,
    // Старые endpoints (для совместимости)
    generateProblem: `${API_BASE_URL}/api/problems/generate/`,
    submitAnswer: `${API_BASE_URL}/api/problems/submit/`,
    leaderboard: `${API_BASE_URL}/api/arena/leaderboard/`,
    arenaStats: `${API_BASE_URL}/api/arena/stats/`,
};

// Настройка: использовать ли Gemini AI (по умолчанию true)
const USE_GEMINI_AI = true;

// Global State
let currentUser = null;
let currentProblem = null;

// Utility Functions
function setAuthMessage(message, isError = false) {
    const msgElement = document.getElementById('authMessage');
    msgElement.textContent = message;
    msgElement.className = `mt-4 text-center text-sm font-medium ${isError ? 'text-red-500' : 'text-green-500'}`;
}

function showLoading(buttonId, textId) {
    const btn = document.getElementById(buttonId);
    const text = document.getElementById(textId);
    if (btn && text) {
        btn.disabled = true;
        text.innerHTML = '<span class="loading"></span>';
    }
}

function hideLoading(buttonId, textId, originalText) {
    const btn = document.getElementById(buttonId);
    const text = document.getElementById(textId);
    if (btn && text) {
        btn.disabled = false;
        text.textContent = originalText;
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function apiRequest(url, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    // Добавляем CSRF токен для POST/PUT/DELETE запросов
    if (options.method && options.method !== 'GET') {
        headers['X-CSRFToken'] = getCookie('csrftoken');
    }

    try {
        const response = await fetch(url, {
            ...options,
            headers,
            credentials: 'include',  // Важно для сессий!
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || data.detail || 'Произошла ошибка');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Authentication Functions
async function handleRegister(e) {
    e.preventDefault();
    setAuthMessage('Регистрация...');

    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const password2 = document.getElementById('registerPassword2').value;

    if (password !== password2) {
        setAuthMessage('Пароли не совпадают', true);
        return;
    }

    try {
        const response = await apiRequest(API_ENDPOINTS.register, {
            method: 'POST',
            body: JSON.stringify({ 
                username, 
                email, 
                password, 
                password2,
            }),
        });

        // Сохраняем данные пользователя (объединяем user и profile)
        currentUser = {
            ...response.user,
            ...response.profile
        };

        // Показываем основной интерфейс
        document.getElementById('authModal').classList.add('hidden');
        document.getElementById('navbar').classList.remove('hidden');
        document.getElementById('mainContent').classList.remove('hidden');

        // Обновляем UI
        updateUserInfo();
        await loadNewProblem();
        await loadProgress();
        
        // Рендерим математические формулы
        renderMath();
        
        // Переключаем на вкладку профиля
        setTimeout(() => {
            document.querySelector('[data-tab="tab-profile"]').click();
            alert('👋 Добро пожаловать! Пожалуйста, заполните информацию о себе в профиле.');
        }, 500);
    } catch (error) {
        setAuthMessage(error.message, true);
    }
}

async function handleLogin(e) {
    e.preventDefault();
    setAuthMessage('Вход...');

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await apiRequest(API_ENDPOINTS.login, {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
        
        // Сохраняем данные пользователя (объединяем user и profile)
        currentUser = {
            ...response.user,
            ...response.profile
        };

        // Показываем основной интерфейс
        document.getElementById('authModal').classList.add('hidden');
        document.getElementById('navbar').classList.remove('hidden');
        document.getElementById('mainContent').classList.remove('hidden');

        // Обновляем UI
        updateUserInfo();
        await loadNewProblem();
        await loadProgress();
        
        // Рендерим математические формулы
        renderMath();
    } catch (error) {
        console.error('Login error:', error);
        setAuthMessage(error.message, true);
    }
}

async function handleLogout() {
    try {
        await apiRequest(API_ENDPOINTS.logout, {
            method: 'POST',
        });
    } catch (error) {
        console.error('Logout error:', error);
    }

    currentUser = null;

    document.getElementById('authModal').classList.remove('hidden');
    document.getElementById('navbar').classList.add('hidden');
    document.getElementById('mainContent').classList.add('hidden');
    
    setAuthMessage('');
}

function toggleAuthView(view) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const authTitle = document.getElementById('authTitle');

    if (view === 'register') {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        authTitle.textContent = 'Регистрация';
    } else {
        registerForm.classList.add('hidden');
        loginForm.classList.remove('hidden');
        authTitle.textContent = 'Вход';
    }
    setAuthMessage('');
}

// App Initialization
async function initializeApp() {
    try {
        // Загружаем профиль пользователя
        const profileData = await apiRequest(API_ENDPOINTS.profile);
        currentUser = profileData;

        // Показываем основной интерфейс
        document.getElementById('authModal').classList.add('hidden');
        document.getElementById('navbar').classList.remove('hidden');
        document.getElementById('mainContent').classList.remove('hidden');

        // Обновляем UI
        updateUserInfo();
        await loadNewProblem();
        await loadProgress();
        
        // Рендерим математические формулы
        renderMath();
    } catch (error) {
        console.error('Initialization error:', error);
        // Не вызываем handleLogout, просто показываем форму входа
        document.getElementById('authModal').classList.remove('hidden');
        document.getElementById('navbar').classList.add('hidden');
        document.getElementById('mainContent').classList.add('hidden');
        throw error; // Пробрасываем ошибку дальше
    }
}

function updateUserInfo() {
    if (!currentUser) return;
    
    const userInfo = document.getElementById('userInfo');
    const profileUsername = document.getElementById('profileUsername');
    const profileEmail = document.getElementById('profileEmail');
    const profileCountry = document.getElementById('profileCountry');
    const profileInitial = document.getElementById('profileInitial');
    const profileIndex = document.getElementById('profileIndex');
    const profileRank = document.getElementById('profileRank');
    const profileDivision = document.getElementById('profileDivision');
    const profileSolved = document.getElementById('profileSolved');

    const countryNames = {
        'RU': 'Россия',
        'KZ': 'Казахстан',
        'UZ': 'Узбекистан',
        'KG': 'Кыргызстан',
        'TJ': 'Таджикистан',
        'UA': 'Украина',
        'BY': 'Беларусь',
        'AZ': 'Азербайджан',
        'OTHER': 'Другая'
    };
    
    const userTypeNames = {
        'student': 'Ученик',
        'teacher': 'Учитель',
        'university': 'Студент',
        'other': 'Другое'
    };

    // Основная информация
    const userTypeText = userTypeNames[currentUser.user_type] || currentUser.user_type;
    const gradeText = currentUser.grade_display || 'Не указано';
    
    if (userInfo) userInfo.textContent = `${currentUser.username} | ${userTypeText} | ${gradeText}`;
    if (profileUsername) profileUsername.textContent = currentUser.username;
    if (profileEmail) profileEmail.textContent = currentUser.email;
    
    // Расширенная информация профиля
    let profileInfo = `Страна: ${countryNames[currentUser.country] || currentUser.country}`;
    if (currentUser.city) profileInfo += ` | Город: ${currentUser.city}`;
    if (currentUser.school) profileInfo += ` | ${currentUser.school}`;
    profileInfo += ` | Возраст: ${currentUser.age}`;
    if (currentUser.grade) profileInfo += ` | Класс: ${currentUser.grade}`;
    
    if (profileCountry) profileCountry.textContent = profileInfo;
    if (profileInitial) profileInitial.textContent = currentUser.username.charAt(0).toUpperCase();
    if (profileIndex) profileIndex.textContent = currentUser.al_khwarizmi_index;
    if (profileRank) profileRank.textContent = currentUser.rank_title;
    if (profileDivision) profileDivision.textContent = currentUser.division;
    if (profileSolved) profileSolved.textContent = currentUser.total_solved_problems || 0;
    
    // Обновляем индекс на дашборде
    updateDashboardIndex();
    
    // Загружаем очки арены
    loadArenaScore();
}

// Обновление индекса и прогресса дивизиона на дашборде
function updateDashboardIndex() {
    const userIndex = document.getElementById('userIndex');
    const userDivision = document.getElementById('userDivision');
    const indexToNext = document.getElementById('indexToNext');
    const divisionProgress = document.getElementById('divisionProgress');
    const divisionInfo = document.getElementById('divisionInfo');
    
    if (!currentUser) return;
    
    const index = currentUser.al_khwarizmi_index || 1000;
    
    // Определяем дивизион и границы
    let divisionName = '';
    let currentMin = 0;
    let nextMin = 0;
    let emoji = '';
    
    if (index < 500) {
        divisionName = 'Лига Новичков';
        currentMin = 0;
        nextMin = 500;
        emoji = '🌱';
    } else if (index < 1550) {
        divisionName = 'Лига Евклида';
        currentMin = 500;
        nextMin = 1550;
        emoji = '📐';
    } else {
        divisionName = 'Лига Эйнштейна';
        currentMin = 1550;
        nextMin = null; // Максимальный дивизион
        emoji = '🧠';
    }
    
    // Обновляем элементы
    if (userIndex) userIndex.textContent = index;
    if (userDivision) userDivision.textContent = `${emoji} ${divisionName}`;
    
    // Прогресс до следующего дивизиона
    if (nextMin) {
        const remaining = nextMin - index;
        const total = nextMin - currentMin;
        const progress = ((index - currentMin) / total) * 100;
        
        if (indexToNext) indexToNext.textContent = `+${remaining}`;
        if (divisionProgress) divisionProgress.style.width = `${Math.min(progress, 100)}%`;
        
        if (divisionInfo) {
            const tasksNeeded = Math.ceil(remaining / 9); // Примерно +9 за задачу
            divisionInfo.textContent = `≈ ${tasksNeeded} задач до следующей лиги`;
        }
    } else {
        // Максимальный дивизион
        if (indexToNext) indexToNext.textContent = '🏆 Максимум';
        if (divisionProgress) divisionProgress.style.width = '100%';
        if (divisionInfo) divisionInfo.textContent = 'Вы в высшей лиге!';
    }
}

// Загрузка очков арены
async function loadArenaScore() {
    const weeklyScore = document.getElementById('weeklyScore');
    
    if (!weeklyScore) return;
    
    try {
        const data = await apiRequest(API_ENDPOINTS.arenaStats);
        if (weeklyScore) weeklyScore.textContent = data.weekly_score || 0;
    } catch (error) {
        console.error('Arena score error:', error);
        if (weeklyScore) weeklyScore.textContent = '0';
    }
}

// Profile Functions
function loadProfileForm() {
    // Заполняем форму текущими данными
    if (currentUser) {
        document.getElementById('profileUserType').value = currentUser.user_type || 'student';
        document.getElementById('profileAge').value = currentUser.age || '';
        document.getElementById('profileGrade').value = currentUser.grade || '';
        document.getElementById('profileSchool').value = currentUser.school || '';
        document.getElementById('profileCity').value = currentUser.city || '';
        document.getElementById('profileCountrySelect').value = currentUser.country || 'KZ';
        
        // Показать/скрыть поле класса
        const gradeContainer = document.getElementById('profileGradeContainer');
        if (currentUser.user_type === 'student') {
            gradeContainer.style.display = 'block';
        } else {
            gradeContainer.style.display = 'none';
        }
    }
}

async function handleProfileSave(e) {
    e.preventDefault();
    
    const messageEl = document.getElementById('profileMessage');
    const btnText = document.getElementById('profileSaveBtnText');
    
    messageEl.textContent = 'Сохранение...';
    messageEl.className = 'text-center text-sm font-medium text-blue-600';
    btnText.textContent = '⏳ Сохранение...';
    
    const user_type = document.getElementById('profileUserType').value;
    const age = parseInt(document.getElementById('profileAge').value);
    const grade = document.getElementById('profileGrade').value || null;
    const school = document.getElementById('profileSchool').value || '';
    const city = document.getElementById('profileCity').value || '';
    const country = document.getElementById('profileCountrySelect').value;
    
    if (!age || age < 5 || age > 100) {
        messageEl.textContent = 'Укажите корректный возраст (5-100)';
        messageEl.className = 'text-center text-sm font-medium text-red-600';
        btnText.textContent = '💾 Сохранить изменения';
        return;
    }
    
    try {
        const data = await apiRequest(API_ENDPOINTS.profile, {
            method: 'PUT',
            body: JSON.stringify({
                user_type,
                age,
                grade: grade ? parseInt(grade) : null,
                school,
                city,
                country
            }),
        });
        
        // Обновляем текущие данные пользователя
        currentUser = data;
        updateUserInfo();
        
        messageEl.textContent = '✅ Профиль успешно обновлен!';
        messageEl.className = 'text-center text-sm font-medium text-green-600';
        btnText.textContent = '💾 Сохранить изменения';
        
        // Очищаем сообщение через 3 секунды
        setTimeout(() => {
            messageEl.textContent = '';
        }, 3000);
        
    } catch (error) {
        messageEl.textContent = `Ошибка: ${error.message}`;
        messageEl.className = 'text-center text-sm font-medium text-red-600';
        btnText.textContent = '💾 Сохранить изменения';
    }
}

// Problem Functions
async function loadNewProblem() {
    const container = document.getElementById('problemContainer');
    
    // Проверяем заполненность профиля
    if (!isProfileComplete()) {
        showProfileIncompleteMessage(container);
        return;
    }
    
    container.innerHTML = '<div class="text-center text-slate-500">🤖 ИИ генерирует задачу специально для вас...</div>';

    try {
        // Используем Gemini AI или статические задачи
        const endpoint = USE_GEMINI_AI ? API_ENDPOINTS.generateProblemAI : API_ENDPOINTS.generateProblem;
        const data = await apiRequest(endpoint);
        currentProblem = data.problem;

        const aiLabel = currentProblem.generated_by_ai ? '🤖 Сгенерировано ИИ' : 'Задача из базы';
        
        container.innerHTML = `
            <div class="flex justify-between items-start mb-3">
                <h3 class="text-lg font-semibold text-blue-800">${currentProblem.title}</h3>
                <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">${aiLabel}</span>
            </div>
            <p class="text-slate-700 mb-4 leading-relaxed">${wrapLatexCommands(currentProblem.description)}</p>
            <div class="text-center my-4 text-xl">
                $$${currentProblem.latex_formula}$$
            </div>
            <p class="text-sm text-slate-500">Тема: ${currentProblem.topic_name} | Сложность: ${currentProblem.difficulty_score}</p>
        `;

        // Очищаем предыдущие результаты
        document.getElementById('feedback').classList.add('hidden');
        document.getElementById('solutionExplanation').classList.add('hidden');
        document.getElementById('helpContent').classList.add('hidden');
        document.getElementById('answerInput').value = '';
        document.getElementById('photoSolutionInput').value = '';
        document.getElementById('fileNameDisplay').classList.add('hidden');

        renderMath();
    } catch (error) {
        // Проверяем, не связана ли ошибка с незаполненным профилем
        if (error.message.includes('Профиль не заполнен') || error.message.includes('profile_incomplete')) {
            showProfileIncompleteMessage(container);
        } else {
            container.innerHTML = `<div class="text-center text-red-500">❌ Ошибка загрузки задачи: ${error.message}<br><small class="text-slate-500">Проверьте настройку GEMINI_API_KEY</small></div>`;
        }
    }
}

// Проверка заполненности профиля
function isProfileComplete() {
    if (!currentUser) return false;
    
    // Проверяем обязательные поля
    if (!currentUser.user_type || !currentUser.age || !currentUser.country) {
        return false;
    }
    
    // Для студентов обязателен класс
    if (currentUser.user_type === 'student' && !currentUser.grade) {
        return false;
    }
    
    return true;
}

// Показать сообщение о незаполненном профиле
function showProfileIncompleteMessage(container) {
    container.innerHTML = `
        <div class="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg">
            <div class="flex items-start">
                <div class="flex-shrink-0">
                    <svg class="h-8 w-8 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                    </svg>
                </div>
                <div class="ml-4">
                    <h3 class="text-lg font-semibold text-yellow-800 mb-2">⚠️ Профиль не заполнен</h3>
                    <p class="text-yellow-700 mb-4">
                        Для решения задач необходимо заполнить профиль. Пожалуйста, укажите:
                    </p>
                    <ul class="list-disc list-inside text-yellow-700 mb-4 space-y-1">
                        <li>Тип пользователя</li>
                        <li>Возраст</li>
                        <li>Страну</li>
                        ${currentUser && currentUser.user_type === 'student' ? '<li>Класс (для учеников)</li>' : ''}
                    </ul>
                    <button 
                        onclick="switchToProfile()" 
                        class="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold px-6 py-2 rounded-lg transition-colors"
                    >
                        👤 Перейти к профилю
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Переключиться на вкладку профиля
function switchToProfile() {
    const profileTab = document.querySelector('[data-tab="tab-profile"]');
    if (profileTab) {
        profileTab.click();
    }
}

async function submitAnswer() {
    const answerInput = document.getElementById('answerInput');
    const photoInput = document.getElementById('photoSolutionInput');
    const feedback = document.getElementById('feedback');

    const answer = answerInput.value.trim();
    const photo = photoInput.files[0];

    if (!answer && !photo) {
        feedback.textContent = 'Введите ответ или загрузите фото решения!';
        feedback.className = 'mt-4 font-semibold text-slate-500';
        feedback.classList.remove('hidden');
        return;
    }

    feedback.textContent = USE_GEMINI_AI ? '🤖 ИИ проверяет ваше решение...' : '⏳ Проверка...';
    feedback.className = 'mt-4 font-semibold text-blue-600';
    feedback.classList.remove('hidden');

    try {
        const formData = new FormData();
        formData.append('problem_id', currentProblem.id);
        if (answer) formData.append('submitted_answer', answer);
        if (photo) formData.append('solution_photo', photo);

        // Используем Gemini AI или обычную проверку
        const endpoint = USE_GEMINI_AI ? API_ENDPOINTS.submitAnswerAI : API_ENDPOINTS.submitAnswer;
        const response = await fetch(endpoint, {
            method: 'POST',
            credentials: 'include',  // Используем сессии вместо токенов
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),  // Добавляем CSRF токен
            },
            body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Ошибка отправки');
        }

        // Обновляем индекс пользователя
        currentUser.al_khwarizmi_index = data.new_index;
        currentUser.total_solved_problems += data.is_correct ? 1 : 0;
        updateUserInfo();

        // Показываем результат
        showSolutionFeedback(data);
        
        // Обновляем прогресс после решения задачи
        await loadProgress();

    } catch (error) {
        feedback.textContent = `Ошибка: ${error.message}`;
        feedback.className = 'mt-4 font-semibold text-red-600';
    }
}

function showSolutionFeedback(data) {
    const feedback = document.getElementById('feedback');
    const explanation = document.getElementById('solutionExplanation');
    const explanationTitle = document.getElementById('explanationTitle');
    const explanationContent = document.getElementById('explanationContent');
    const pointsEarned = document.getElementById('pointsEarned');

    if (data.is_correct) {
        feedback.textContent = '✅ Правильно! Отличная работа!';
        feedback.className = 'mt-4 font-semibold text-green-600';
        explanationTitle.textContent = '✅ Решение верно! Разбор:';
        explanation.style.backgroundColor = '#f0fdf4';
        explanation.style.borderColor = '#4ade80';
    } else {
        feedback.textContent = '❌ Неверно. Изучите разбор ниже.';
        feedback.className = 'mt-4 font-semibold text-red-600';
        explanationTitle.textContent = '❌ Правильное решение:';
        explanation.style.backgroundColor = '#fef2f2';
        explanation.style.borderColor = '#f87171';
    }

    // Показываем шаги решения
    let stepsHTML = '<h4 class="font-semibold text-slate-800 mb-3">Пошаговое решение:</h4><ol class="list-decimal list-inside ml-4 space-y-3">';
    data.solution_steps.forEach(step => {
        stepsHTML += `<li class="text-slate-700 text-base leading-relaxed">${wrapLatexCommands(step)}</li>`;
    });
    stepsHTML += '</ol>';
    
    stepsHTML += `<p class="mt-4 text-base text-slate-700"><strong>Правильный ответ:</strong> ${wrapLatexCommands(data.correct_answer)}</p>`;

    explanationContent.innerHTML = stepsHTML;
    
    const indexChange = data.index_change > 0 ? `+${data.index_change}` : data.index_change;
    pointsEarned.textContent = `Начислено: ${data.points_awarded} очков | Изменение индекса: ${indexChange}`;
    pointsEarned.className = data.is_correct ? 'mt-4 text-sm font-semibold text-green-700' : 'mt-4 text-sm font-semibold text-red-700';

    explanation.classList.remove('hidden');
    renderMath();
}

function toggleHelp() {
    const helpContent = document.getElementById('helpContent');
    const helpBtn = document.getElementById('helpBtn');
    const hintsContainer = document.getElementById('hintsContainer');

    if (helpContent.classList.contains('hidden')) {
        // Показываем подсказки
        if (currentProblem && currentProblem.hints) {
            let hintsHTML = '<ul class="list-disc list-inside text-slate-700 ml-4 space-y-3">';
            currentProblem.hints.forEach(hint => {
                hintsHTML += `<li class="text-base leading-relaxed">${wrapLatexCommands(hint)}</li>`;
            });
            hintsHTML += '</ul>';
            hintsContainer.innerHTML = hintsHTML;
            
            // Рендерим математические формулы в подсказках
            renderMath();
        } else {
            hintsContainer.innerHTML = '<p class="text-slate-600">Подсказки недоступны для этой задачи.</p>';
        }
        helpContent.classList.remove('hidden');
        helpBtn.textContent = 'Скрыть подсказки';
    } else {
        helpContent.classList.add('hidden');
        helpBtn.textContent = '💡 Помощь';
    }
}

function displayFileName() {
    const input = document.getElementById('photoSolutionInput');
    const display = document.getElementById('fileNameDisplay');
    const fileNameSpan = display.querySelector('span');

    if (input.files.length > 0) {
        fileNameSpan.textContent = input.files[0].name;
        display.classList.remove('hidden');
    } else {
        display.classList.add('hidden');
    }
}

// Progress Functions
async function loadProgress() {
    const container = document.getElementById('progressContainer');

    try {
        const data = await apiRequest(API_ENDPOINTS.progress);

        if (data.length === 0) {
            container.innerHTML = '<p class="text-center text-slate-500">Пока нет данных о прогрессе</p>';
            return;
        }

        let html = '';
        data.forEach(topic => {
            const color = topic.success_rate >= 70 ? '#22c55e' : topic.success_rate >= 50 ? '#f97316' : '#ef4444';
            html += `
                <div>
                    <div class="flex justify-between text-sm text-slate-600 mb-1">
                        <span>${topic.topic_name}</span>
                        <span>${topic.success_rate}%</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" style="width: ${topic.success_rate}%; background-color: ${color};"></div>
                    </div>
                    <p class="text-xs text-slate-500 mt-1">${topic.correct_attempts}/${topic.total_attempts} решено</p>
                </div>
            `;
        });

        container.innerHTML = html;
    } catch (error) {
        container.innerHTML = `<p class="text-center text-red-500">Ошибка: ${error.message}</p>`;
    }
}

// Arena Functions
async function loadArenaData() {
    try {
        const [leaderboardData, statsData] = await Promise.all([
            apiRequest(API_ENDPOINTS.leaderboard),
            apiRequest(API_ENDPOINTS.arenaStats),
        ]);

        // Обновляем дивизион
        const divisionNames = {
            'NOVICE': 'Лига Новичков',
            'EUCLID': 'Лига Евклида',
            'EINSTEIN': 'Лига Эйнштейна'
        };
        document.getElementById('arenaDivision').textContent = divisionNames[statsData.current_division] || statsData.current_division;

        // Обновляем статистику
        const arenaStats = document.getElementById('arenaStats');
        arenaStats.innerHTML = `
            <div class="p-4 bg-yellow-50 rounded-lg text-center border border-yellow-300">
                <p class="text-xl font-bold text-yellow-700">#${statsData.rank || '—'}</p>
                <p class="text-sm text-slate-600">Ваше место</p>
            </div>
            <div class="p-4 bg-slate-100 rounded-lg text-center border border-slate-300">
                <p class="text-xl font-bold text-slate-700">🏆 ${statsData.total_cups || 0}</p>
                <p class="text-sm text-slate-600">Кубков</p>
            </div>
            <div class="p-4 bg-slate-100 rounded-lg text-center border border-slate-300">
                <p class="text-xl font-bold text-slate-700">🥇 ${statsData.total_medals || 0}</p>
                <p class="text-sm text-slate-600">Медалей</p>
            </div>
        `;

        // Обновляем таблицу лидеров
        const leaderboardBody = document.getElementById('leaderboardBody');
        if (leaderboardData.leaderboard.length === 0) {
            leaderboardBody.innerHTML = '<tr><td colspan="4" class="px-6 py-4 text-center text-slate-500">Нет данных</td></tr>';
            return;
        }

        let html = '';
        leaderboardData.leaderboard.forEach((player, index) => {
            const isCurrentUser = player.username === currentUser.username;
            const rowClass = isCurrentUser ? 'bg-blue-50 font-semibold' : '';
            html += `
                <tr class="${rowClass}">
                    <td class="px-6 py-4 whitespace-nowrap ${index < 3 ? 'font-bold' : ''}">${player.rank}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${player.username}${isCurrentUser ? ' (Вы)' : ''}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${player.current_index}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${player.weekly_score}</td>
                </tr>
            `;
        });

        leaderboardBody.innerHTML = html;
    } catch (error) {
        console.error('Arena error:', error);
    }
}

// Tab Navigation
function setupTabs() {
    const navButtons = document.querySelectorAll('.nav-link');
    const tabContents = document.querySelectorAll('.tab-content');

    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');

            // Скрываем все табы
            tabContents.forEach(content => content.classList.add('hidden'));
            navButtons.forEach(btn => btn.classList.remove('active'));

            // Показываем выбранный таб
            document.getElementById(tabId).classList.remove('hidden');
            button.classList.add('active');

            // Загружаем данные при переключении табов
            if (tabId === 'tab-arena') {
                loadArenaData();
            } else if (tabId === 'tab-profile') {
                loadProfileForm();
            }
        });
    });
}

// Math Rendering Helper - оборачивает LaTeX команды в $ для KaTeX
function wrapLatexCommands(text) {
    // Проверяем, что text - строка, иначе возвращаем как есть
    if (!text || typeof text !== 'string') {
        return text || '';
    }
    
    // Если текст уже содержит $ или $$, возвращаем как есть
    if (text.includes('$')) {
        return text;
    }
    
    // Паттерн для поиска LaTeX команд: \command{...} или \command
    // Например: \frac{1}{3}, \times, \sqrt{2}
    const latexPattern = /\\[a-zA-Z]+(\{[^}]*\})?/g;
    
    // Проверяем, есть ли LaTeX команды
    if (latexPattern.test(text)) {
        // Оборачиваем весь текст в $, так как он содержит LaTeX
        return `$${text}$`;
    }
    
    return text;
}

// Math Rendering
function renderMath() {
    if (typeof renderMathInElement !== 'undefined') {
        renderMathInElement(document.body, {
            delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '$', right: '$', display: false }
            ],
            throwOnError: false
        });
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', async () => {
    const loadingScreen = document.getElementById('loadingScreen');
    const authModal = document.getElementById('authModal');
    const navbar = document.getElementById('navbar');
    const mainContent = document.getElementById('mainContent');
    
    // Получаем CSRF токен
    try {
        await fetch(API_ENDPOINTS.csrf, { credentials: 'include' });
    } catch (error) {
        console.error('CSRF token error:', error);
    }
    
    // Формы аутентификации
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
    
    // Форма профиля
    document.getElementById('profileEditForm')?.addEventListener('submit', handleProfileSave);

    // Навигация
    setupTabs();

    // Проверяем, есть ли активная сессия
    try {
        const response = await fetch(API_ENDPOINTS.profile, {
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            // Есть активная сессия - загружаем профиль
            const data = await response.json();
            
            // Сохраняем данные пользователя
            currentUser = {
                ...data.user,
                ...data.profile
            };
            
            // Обновляем UI
            updateUserInfo();
            await loadNewProblem();
            await loadProgress();
            
            // Плавно скрываем загрузку и показываем контент
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.classList.add('hidden');
                navbar.classList.remove('hidden');
                mainContent.classList.remove('hidden');
            }, 300);
            
            // Рендерим математические формулы
            renderMath();
        } else {
            // Нет активной сессии - показываем форму входа
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.classList.add('hidden');
                authModal.classList.remove('hidden');
            }, 300);
            setAuthMessage('Добро пожаловать! Войдите или зарегистрируйтесь.', false);
        }
    } catch (error) {
        // Ошибка при проверке сессии - показываем форму входа
        console.log('Нет активной сессии:', error);
        loadingScreen.style.opacity = '0';
        setTimeout(() => {
            loadingScreen.classList.add('hidden');
            authModal.classList.remove('hidden');
        }, 300);
        setAuthMessage('Добро пожаловать! Войдите или зарегистрируйтесь.', false);
    }
});

// Экспорт функций для использования в HTML
window.toggleAuthView = toggleAuthView;
window.handleLogout = handleLogout;
window.loadNewProblem = loadNewProblem;
window.submitAnswer = submitAnswer;
window.toggleHelp = toggleHelp;
window.displayFileName = displayFileName;
window.switchToProfile = switchToProfile;
