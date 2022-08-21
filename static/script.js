const $createButton = document.querySelector(".create-button");
const $articleList = document.querySelector(".article-list");
const $noArticle = document.querySelector(".no-article");
const $articleForm = document.querySelector(".article-form");
const $article = document.querySelector(".article");
const $updateButton = document.querySelector(".update-button");
const $deleteButton = document.querySelector(".delete-button");
const $articleTitle = document.querySelector(".article-title");
const $articleID = document.querySelector(".article-id");
const $articleDesrciption = document.querySelector(".article-description");
const $articleUpdateForm = document.querySelector(".article-update-form");
const $articleUpdateTitle = document.querySelector(".update-title");
const $articleUpdateDesrciption = document.querySelector(".update-description");

window.addEventListener("load", (e) => {
  makeArticleList();
});

const getArticles = async () => {
  const response = await axios.get("http://127.0.0.1:8000/articles");
  return response.data;
};

const showArticle = async (id) => {
  const response = await axios.get(`http://127.0.0.1:8000/article/${id}`);
  article = response.data;
  $article.classList.remove("hide");
  $articleTitle.innerText = `${article.title}`;
  $articleID.innerText = `${article.id}`;
  $articleID.id = article.id;
  $articleDesrciption.innerText = `${article.description}`;
};

const makeArticleList = async () => {
  $articleList.innerHTML = "";
  const articles = await getArticles();
  if (articles.length == 0) {
    $noArticle.classList.remove("hide");
  } else {
    articles.map((article) => {
      const articleNode = document.createElement("li");
      articleNode.innerText = article.title;
      articleNode.classList.add(article.id);
      articleNode.style.cursor = "pointer";
      articleNode.addEventListener("click", () => {
        showArticle(article.id);
      });

      $articleList.appendChild(articleNode);
    });
  }
};

const updateArticle = async (id, title, description) => {
  const response = await axios.put(`http://127.0.0.1:8000/article/${id}`, { title, description });
  return response.data;
};

$articleUpdateForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  await updateArticle($articleID.id, $articleUpdateTitle.value, $articleUpdateDesrciption.value);
  $articleUpdateForm.classList.add("hide");
  $articleUpdateTitle.value = "";
  $articleUpdateDesrciption.value = "";
  makeArticleList();
});

$updateButton.addEventListener("click", (e) => {
  $article.classList.add("hide");
  $articleUpdateForm.classList.remove("hide");
  $articleUpdateTitle.value = $articleTitle.innerText;
  $articleUpdateDesrciption.value = $articleDesrciption.innerText;
});

const deleteArticle = async (id) => {
  const response = await axios.delete(`http://127.0.0.1:8000/article/${id}`);
  return response.data;
};

$deleteButton.addEventListener("click", async (e) => {
  const articleID = $article.querySelector(".article-id").id;
  try {
    await deleteArticle(articleID);
    $article.classList.add("hide");
    makeArticleList();
  } catch {
    alert("글 삭제 중 에러가 발생하였습니다");
  }
});

$createButton.addEventListener("click", (e) => {
  $articleForm.classList.remove("hide");
});

const postArticle = async (title, description) => {
  const response = await axios.post("http://127.0.0.1:8000/article", {
    title,
    description,
  });
  return response.data;
};

$articleForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const $title = e.target.querySelector(".title");
  const $description = e.target.querySelector(".description");

  await postArticle($title.value, $description.value);
  $articleForm.classList.add("hide");
  $title.value = "";
  $description.value = "";
  makeArticleList();
});
