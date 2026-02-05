document.addEventListener('DOMContentLoaded', () => {
    // URLパラメータから検索クエリを取得
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('search');

    if (query) {
        // スペースや読点、中黒などでキーワードを分割し、小文字化して配列を作成
        const keywords = query.replace(/[ 　・／,，]/g, ' ').toLowerCase().split(' ').filter(k => k.length > 0);

        // 検索結果タイトルを更新
        const searchTitle = document.getElementById('search-results-title');
        if (searchTitle) {
            searchTitle.textContent = `「${query}」の検索結果`;
        }

        // 検索フォームに値をセット
        const searchInputs = document.querySelectorAll('.search-input');
        searchInputs.forEach(input => input.value = query);

        // 記事カードを取得
        const articles = document.querySelectorAll('.post-card');
        let hitCount = 0;

        articles.forEach(article => {
            const titleElement = article.querySelector('h3');
            const excerptElement = article.querySelector('.excerpt');
            const categoryElement = article.querySelector('.category');

            const title = titleElement ? titleElement.textContent.toLowerCase() : '';
            const excerpt = excerptElement ? excerptElement.textContent.toLowerCase() : '';

            // 全てのカテゴリタグからテキストを取得
            const categoryElements = article.querySelectorAll('.category');
            const categories = Array.from(categoryElements).map(el => el.textContent.trim().toLowerCase()).join(' ');

            // AND検索: すべてのキーワードが含まれているかチェック
            const isMatch = keywords.every(keyword =>
                title.includes(keyword) ||
                excerpt.includes(keyword) ||
                categories.includes(keyword)
            );

            if (isMatch) {
                article.style.display = 'flex'; // またはblockなど、元のdisplayに合わせて
                hitCount++;
            } else {
                article.style.display = 'none';
            }
        });

        // 検索結果がない場合のメッセージ
        if (hitCount === 0) {
            const noResultsMessage = document.createElement('p');
            noResultsMessage.textContent = '該当する記事は見つかりませんでした。';
            noResultsMessage.style.textAlign = 'center';
            noResultsMessage.style.marginTop = '20px';

            // 記事リストの親要素に追加（必要に応じて調整）
            const mainContent = document.querySelector('.main-content');
            mainContent.appendChild(noResultsMessage);
        }

    } else {
        // クエリがない場合は全記事を表示するか、検索を促すメッセージを表示
        // ここではタイトルを変更のみ
        const searchTitle = document.getElementById('search-results-title');
        if (searchTitle) {
            searchTitle.textContent = 'キーワードを入力してください';
        }
    }
});
