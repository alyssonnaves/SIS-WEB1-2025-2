const BASE_URL = "http://127.0.0.1:8000/v1";

const elCatList = document.getElementById("categorias-list");
const elProdList = document.getElementById("produtos-list");
const elCatForm = document.getElementById("form-categoria");
const elProdForm = document.getElementById("form-produto");
const elProdCategoria = document.getElementById("prod-categoria");

// --------- Helpers -----------
async function http(method, url, body) {
  const opt = { method, headers: { "Content-Type": "application/json" } };
  if (body) opt.body = JSON.stringify(body);
  const res = await fetch(url, opt);
  if (!res.ok) {
    const detail = await safeJson(res);
    throw new Error(detail?.detail || `Erro HTTP ${res.status}`);
  }
  return safeJson(res);
}
async function safeJson(res) {
  try { return await res.json(); } catch { return null; }
}
function money(n) {
  const v = Number(n ?? 0);
  return v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

// --------- Categorias ----------
async function loadCategorias() {
  const data = await http("GET", `${BASE_URL}/categoria`);
  renderCategorias(data);
  fillCategoriaSelect(data);
}
function renderCategorias(items = []) {
  elCatList.innerHTML = "";
  if (!items.length) {
    elCatList.innerHTML = `<div class="item"><span>Nenhuma categoria cadastrada.</span></div>`;
    return;
  }
  for (const c of items) {
    const div = document.createElement("div");
    div.className = "item";
    div.innerHTML = `
      <div>
        <strong>${escapeHtml(c.nome)}</strong>
        <div class="badge">#${c.id}</div>
      </div>
      <div class="actions">
        <button class="btn-danger" onclick="deleteCategoria(${c.id})">Excluir</button>
      </div>
    `;
    elCatList.appendChild(div);
  }
}
function fillCategoriaSelect(items = []) {
  elProdCategoria.innerHTML = `<option value="" disabled selected>Selecione...</option>`;
  for (const c of items) {
    const opt = document.createElement("option");
    opt.value = c.id;
    opt.textContent = c.nome;
    elProdCategoria.appendChild(opt);
  }
}
async function createCategoria(nome) {
  await http("POST", `${BASE_URL}/categoria`, { nome });
  await loadCategorias();
}
async function deleteCategoria(id) {
  if (!confirm("Excluir esta categoria?")) return;
  await http("DELETE", `${BASE_URL}/categoria/${id}`);
  await Promise.all([loadCategorias(), loadProdutos()]);
}

// --------- Produtos -----------
async function loadProdutos() {
  const data = await http("GET", `${BASE_URL}/produto`);
  renderProdutos(data);
}
function renderProdutos(items = []) {
  elProdList.innerHTML = "";
  if (!items.length) {
    elProdList.innerHTML = `<div class="item"><span>Nenhum produto cadastrado.</span></div>`;
    return;
  }
  for (const p of items) {
    const div = document.createElement("div");
    div.className = "item";
    div.innerHTML = `
      <div>
        <strong>${escapeHtml(p.nome)}</strong>
        <div class="badge">#${p.id} • ${money(p.preco)} • cat:${p.categoria_id}</div>
      </div>
      <div class="actions">
        <button class="btn-danger" onclick="deleteProduto(${p.id})">Excluir</button>
      </div>
    `;
    elProdList.appendChild(div);
  }
}
async function createProduto({ nome, preco, categoria_id }) {
  await http("POST", `${BASE_URL}/produto`, { nome, preco: Number(preco), categoria_id: Number(categoria_id) });
  await loadProdutos();
}
async function deleteProduto(id) {
  if (!confirm("Excluir este produto?")) return;
  await http("DELETE", `${BASE_URL}/produtos/${id}`);
  await loadProdutos();
}

// --------- Forms -----------
elCatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const nome = document.getElementById("cat-nome").value.trim();
  if (!nome) return alert("Informe o nome da categoria.");
  try {
    await createCategoria(nome);
    elCatForm.reset();
  } catch (err) {
    alert(err.message);
  }
});

elProdForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const nome = document.getElementById("prod-nome").value.trim();
  const preco = document.getElementById("prod-preco").value;
  const categoria_id = document.getElementById("prod-categoria").value;
  if (!nome || !preco || !categoria_id) return alert("Preencha todos os campos.");
  try {
    await createProduto({ nome, preco, categoria_id });
    elProdForm.reset();
    // mantém categorias carregadas
    await Promise.all([loadProdutos(), loadCategorias()]);
  } catch (err) {
    alert(err.message);
  }
});

// --------- Utils -----------
function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"']/g, (m) => (
    { "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[m]
  ));
}

// --------- Init -----------
(async function init() {
  try {
    await loadCategorias();
    await loadProdutos();
  } catch (err) {
    alert("Erro ao conectar na API: " + err.message);
  }
})();
