document.getElementById('file-input').addEventListener('change', function() {
    const fileName = this.files[0] ? this.files[0].name : 'Seçilen dosya yok';
    document.querySelector('.file-name').textContent = fileName;
});
