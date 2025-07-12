// Workshop Inventory Management System - Main JavaScript

$(document).ready(function() {
    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Initialize popovers
    $('[data-bs-toggle="popover"]').popover();
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert-dismissible').fadeOut('slow');
    }, 5000);
    
    // Add loading animation to forms
    $('form').on('submit', function() {
        var submitBtn = $(this).find('button[type="submit"]');
        var originalText = submitBtn.html();
        submitBtn.html('<span class="loading"></span> Processing...');
        submitBtn.prop('disabled', true);
        
        // Re-enable button after 10 seconds (in case of error)
        setTimeout(function() {
            submitBtn.html(originalText);
            submitBtn.prop('disabled', false);
        }, 10000);
    });
    
    // Add confirmation for delete actions
    $('.btn-danger').on('click', function(e) {
        if ($(this).text().toLowerCase().includes('delete')) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        }
    });
    
    // Format numbers with commas
    $('.number-format').each(function() {
        var num = $(this).text();
        if (!isNaN(num) && num !== '') {
            $(this).text(parseInt(num).toLocaleString());
        }
    });
    
    // Add smooth scrolling to anchor links
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        var target = $(this.hash);
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 70
            }, 300);
        }
    });
    
    // Table row highlight on hover
    $('.table tbody tr').on('mouseenter', function() {
        $(this).addClass('table-active');
    }).on('mouseleave', function() {
        $(this).removeClass('table-active');
    });
    
    // Auto-refresh notifications every 30 seconds
    if (window.location.pathname === '/notifications') {
        setInterval(function() {
            location.reload();
        }, 30000);
    }
    
    // Add page transition animation
    $('body').addClass('page-transition');
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize data tables
    initializeDataTables();
});

// Search functionality
function initializeSearch() {
    var searchInput = $('#search');
    var searchTimer;
    
    searchInput.on('input', function() {
        clearTimeout(searchTimer);
        var query = $(this).val();
        
        if (query.length >= 2) {
            searchTimer = setTimeout(function() {
                performSearch(query);
            }, 300);
        } else if (query.length === 0) {
            clearSearchResults();
        }
    });
}

function performSearch(query) {
    // This would be implemented for specific search functionality
    console.log('Searching for:', query);
}

function clearSearchResults() {
    // Clear search results
    console.log('Clearing search results');
}

// Form validation
function initializeFormValidation() {
    $('form').each(function() {
        $(this).on('submit', function(e) {
            var isValid = true;
            
            // Check required fields
            $(this).find('input[required], select[required], textarea[required]').each(function() {
                if ($(this).val() === '') {
                    $(this).addClass('is-invalid');
                    isValid = false;
                } else {
                    $(this).removeClass('is-invalid');
                }
            });
            
            // Check email format
            $(this).find('input[type="email"]').each(function() {
                var email = $(this).val();
                if (email && !isValidEmail(email)) {
                    $(this).addClass('is-invalid');
                    isValid = false;
                } else {
                    $(this).removeClass('is-invalid');
                }
            });
            
            // Check number fields
            $(this).find('input[type="number"]').each(function() {
                var num = $(this).val();
                var min = $(this).attr('min');
                var max = $(this).attr('max');
                
                if (num && min && parseFloat(num) < parseFloat(min)) {
                    $(this).addClass('is-invalid');
                    isValid = false;
                } else if (num && max && parseFloat(num) > parseFloat(max)) {
                    $(this).addClass('is-invalid');
                    isValid = false;
                } else {
                    $(this).removeClass('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill in all required fields correctly.', 'error');
                
                // Focus on first invalid field
                $(this).find('.is-invalid').first().focus();
            }
        });
    });
    
    // Remove validation classes on input
    $('input, select, textarea').on('input change', function() {
        $(this).removeClass('is-invalid is-valid');
    });
}

// Data tables initialization
function initializeDataTables() {
    if ($.fn.DataTable) {
        $('.data-table').DataTable({
            responsive: true,
            pageLength: 25,
            lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
            language: {
                search: "Search records:",
                lengthMenu: "Show _MENU_ records per page",
                info: "Showing _START_ to _END_ of _TOTAL_ records",
                infoEmpty: "No records available",
                infoFiltered: "(filtered from _MAX_ total records)"
            }
        });
    }
}

// Utility functions
function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showNotification(message, type) {
    var alertClass = 'alert-' + (type === 'error' ? 'danger' : type);
    var notification = $('<div class="alert ' + alertClass + ' alert-dismissible fade show" role="alert">' +
        message +
        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
        '</div>');
    
    $('.container').first().prepend(notification);
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        notification.fadeOut('slow', function() {
            $(this).remove();
        });
    }, 5000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    var date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(dateString) {
    var date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Export functionality
function exportToExcel(tableId, filename) {
    var table = document.getElementById(tableId);
    if (!table) return;
    
    var wb = XLSX.utils.table_to_book(table, {sheet: "Sheet1"});
    XLSX.writeFile(wb, filename + '.xlsx');
}

function exportToCSV(tableId, filename) {
    var table = document.getElementById(tableId);
    if (!table) return;
    
    var csv = [];
    var rows = table.querySelectorAll('tr');
    
    for (var i = 0; i < rows.length; i++) {
        var row = [];
        var cols = rows[i].querySelectorAll('td, th');
        
        for (var j = 0; j < cols.length; j++) {
            row.push(cols[j].innerText);
        }
        
        csv.push(row.join(','));
    }
    
    var csvFile = new Blob([csv.join('\n')], {type: 'text/csv'});
    var downloadLink = document.createElement('a');
    downloadLink.download = filename + '.csv';
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// Print functionality
function printPage() {
    window.print();
}

function printTable(tableId) {
    var table = document.getElementById(tableId);
    if (!table) return;
    
    var printWindow = window.open('', '', 'height=600,width=800');
    printWindow.document.write('<html><head><title>Print</title>');
    printWindow.document.write('<style>table{width:100%;border-collapse:collapse;}th,td{border:1px solid #ddd;padding:8px;text-align:left;}th{background-color:#f2f2f2;}</style>');
    printWindow.document.write('</head><body>');
    printWindow.document.write(table.outerHTML);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}

// Theme toggle functionality
function toggleTheme() {
    var body = document.body;
    var currentTheme = body.getAttribute('data-theme');
    var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Initialize theme from localStorage
function initializeTheme() {
    var savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.body.setAttribute('data-theme', savedTheme);
    }
}

// Call initialize theme on page load
initializeTheme();

// Global error handler
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    showNotification('An error occurred. Please try again.', 'error');
});

// AJAX error handler
$(document).ajaxError(function(event, jqXHR, ajaxSettings, thrownError) {
    console.error('AJAX error:', thrownError);
    showNotification('Network error. Please check your connection and try again.', 'error');
});

// Service worker registration (for offline support)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js').then(function(registration) {
            console.log('ServiceWorker registration successful');
        }, function(err) {
            console.log('ServiceWorker registration failed: ', err);
        });
    });
}