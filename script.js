const yearNodes = document.querySelectorAll('#year');
const currentYear = new Date().getFullYear();
yearNodes.forEach((node) => {
  node.textContent = String(currentYear);
});

const filterButtons = document.querySelectorAll('[data-filter]');
const publicationItems = document.querySelectorAll('.paper-item[data-topic]');
const publicationGroups = document.querySelectorAll('.publication-group');

filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;

    filterButtons.forEach((btn) => btn.classList.remove('is-active'));
    button.classList.add('is-active');

    publicationItems.forEach((item) => {
      const topics = item.dataset.topic || '';
      const matches = filter === 'all' || topics.split(/\s+/).includes(filter);
      item.classList.toggle('is-hidden', !matches);
    });

    publicationGroups.forEach((group) => {
      const visibleItems = group.querySelectorAll('.paper-item:not(.is-hidden)');
      group.classList.toggle('is-hidden', visibleItems.length === 0);
    });
  });
});
