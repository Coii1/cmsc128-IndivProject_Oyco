// API Base URL
const API_BASE_URL = 'http://localhost:5000/api';

// State
let tasks = [];
let currentTaskId = null;

// DOM Elements
const taskList = document.getElementById('taskList');
const addTaskInput = document.getElementById('addTaskInput');
const taskDetailSidebar = document.getElementById('taskDetailSidebar');
const overlay = document.getElementById('overlay');
const closeDetailBtn = document.getElementById('closeDetailBtn');
const taskNameInput = document.getElementById('taskNameInput');
const timeInput = document.getElementById('timeInput');
const taskDateInput = document.getElementById('taskDateInput');
const deleteTaskBtn = document.getElementById('deleteTaskBtn');
const createdDate = document.getElementById('createdDate');

// API Functions
async function fetchTasks() {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`);
        if (!response.ok) throw new Error('Failed to fetch tasks');
        tasks = await response.json();
        renderTasks();
    } catch (error) {
        console.error('Error fetching tasks:', error);
        alert('Failed to load tasks. Please refresh the page.');
    }
}

async function createTask(taskData) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(taskData)
        });
        if (!response.ok) throw new Error('Failed to create task');
        const newTask = await response.json();
        tasks.push(newTask);
        renderTasks();
        return newTask;
    } catch (error) {
        console.error('Error creating task:', error);
        alert('Failed to create task. Please try again.');
    }
}

async function updateTask(taskId, updates) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updates)
        });
        if (!response.ok) throw new Error('Failed to update task');
        const updatedTask = await response.json();
        
        // Update local tasks array
        const index = tasks.findIndex(t => t.id === taskId);
        if (index !== -1) {
            tasks[index] = updatedTask;
        }
        renderTasks();
        return updatedTask;
    } catch (error) {
        console.error('Error updating task:', error);
        alert('Failed to update task. Please try again.');
    }
}

async function deleteTaskAPI(taskId) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete task');
        
        // Remove from local array
        tasks = tasks.filter(t => t.id !== taskId);
        renderTasks();
    } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task. Please try again.');
    }
}

// Render tasks
function renderTasks() {
    taskList.innerHTML = '';
    tasks.forEach(task => {
        const taskEl = document.createElement('div');
        taskEl.className = 'task-item';
        taskEl.innerHTML = `
            <div class="task-checkbox ${task.completed ? 'checked' : ''}" data-id="${task.id}"></div>
            <div class="task-content">
                <div class="task-name ${task.completed ? 'completed' : ''}">${task.name}</div>
                ${task.date ? `<div class="task-date">${formatDateDisplay(task.date)}</div>` : ''}
            </div>
            <button class="task-delete" data-id="${task.id}">🗑️</button>
        `;
        
        // Click task to open detail
        taskEl.addEventListener('click', (e) => {
            if (!e.target.classList.contains('task-checkbox') && 
                !e.target.classList.contains('task-delete')) {
                openTaskDetail(task.id);
            }
        });

        // Checkbox toggle
        const checkbox = taskEl.querySelector('.task-checkbox');
        checkbox.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleTaskComplete(task.id);
        });

        // Delete button
        const deleteBtn = taskEl.querySelector('.task-delete');
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            deleteTask(task.id);
        });

        taskList.appendChild(taskEl);
    });
}

// Open task detail sidebar
function openTaskDetail(taskId) {
    currentTaskId = taskId;
    const task = tasks.find(t => t.id === taskId);
    
    if (!task) return;
    
    taskNameInput.value = task.name;
    timeInput.value = task.time || '';
    taskDateInput.value = task.date || '';
    createdDate.textContent = `Created on ${task.createdDate}`;
    
    taskDetailSidebar.classList.add('open');
    overlay.classList.add('active');
}

// Close task detail sidebar
async function closeTaskDetail() {
    if (currentTaskId) {
        const task = tasks.find(t => t.id === currentTaskId);
        
        // Check if anything changed
        const hasChanges = 
            taskNameInput.value !== task.name ||
            timeInput.value !== (task.time || '') ||
            taskDateInput.value !== (task.date || '');
        
        if (hasChanges) {
            // Save changes to backend
            await updateTask(currentTaskId, {
                name: taskNameInput.value.trim() || task.name, // Keep original if empty
                time: timeInput.value,
                date: taskDateInput.value
            });
        }
    }
    
    taskDetailSidebar.classList.remove('open');
    overlay.classList.remove('active');
    currentTaskId = null;
}

// Toggle task completion
async function toggleTaskComplete(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
        await updateTask(taskId, { completed: !task.completed });
    }
}

// Delete task
async function deleteTask(taskId) {
    if (confirm('Are you sure you want to delete this task?')) {
        await deleteTaskAPI(taskId);
        
        if (currentTaskId === taskId) {
            taskDetailSidebar.classList.remove('open');
            overlay.classList.remove('active');
            currentTaskId = null;
        }
    }
}

// Add new task
async function addNewTask() {
    const taskName = addTaskInput.value.trim();
    if (!taskName) return;

    await createTask({ name: taskName });
    addTaskInput.value = '';
}

// Helper functions
function formatDateDisplay(isoDate) {
    if (!isoDate) return '';
    const date = new Date(isoDate);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

// Event listeners
closeDetailBtn.addEventListener('click', closeTaskDetail);
overlay.addEventListener('click', closeTaskDetail);

addTaskInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addNewTask();
    }
});

deleteTaskBtn.addEventListener('click', () => {
    if (currentTaskId) {
        deleteTask(currentTaskId);
    }
});

// Initialize app
fetchTasks();

//undo
//prio, sorting