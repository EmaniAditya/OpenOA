async function getJson(path) {
  const res = await fetch(path);
  if (!res.ok) {
    throw new Error(`${path} -> HTTP ${res.status}`);
  }
  return await res.json();
}

function showError(id, error) {
  document.getElementById(id).textContent = `Error: ${error.message}`;
}

async function load() {
  try {
    const health = await getJson('/api/health');
    document.getElementById('health').textContent = JSON.stringify(health, null, 2);
  } catch (error) {
    showError('health', error);
  }

  try {
    const version = await getJson('/api/version');
    document.getElementById('version').textContent = JSON.stringify(version, null, 2);
  } catch (error) {
    showError('version', error);
  }

  try {
    const methodsData = await getJson('/api/methods');
    const methodsList = document.getElementById('methods');
    methodsList.innerHTML = '';
    for (const method of methodsData.methods || []) {
      const li = document.createElement('li');
      li.textContent = method;
      methodsList.appendChild(li);
    }
  } catch (error) {
    const methodsList = document.getElementById('methods');
    methodsList.innerHTML = `<li>Error: ${error.message}</li>`;
  }
}

load();
