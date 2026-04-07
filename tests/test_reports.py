"""
Unit tests for reports API endpoints.
"""
import json
import pytest
from datetime import date, timedelta


class TestReportsSummary:
    """Tests for reports summary endpoint."""
    
    def test_get_report_summary_monthly(self, client, init_database):
        """Test getting monthly report summary."""
        response = client.get('/api/reports/summary?period=monthly')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'period' in data
        assert data['period'] == 'monthly'
        assert 'total_amount' in data
        assert 'expense_count' in data
        assert 'category_breakdown' in data
        assert 'daily_trend' in data
    
    def test_get_report_summary_daily(self, client, init_database):
        """Test getting daily report summary."""
        response = client.get('/api/reports/summary?period=daily')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['period'] == 'daily'
    
    def test_get_report_summary_weekly(self, client, init_database):
        """Test getting weekly report summary."""
        response = client.get('/api/reports/summary?period=weekly')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['period'] == 'weekly'
    
    def test_get_report_summary_quarterly(self, client, init_database):
        """Test getting quarterly report summary."""
        response = client.get('/api/reports/summary?period=quarterly')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['period'] == 'quarterly'
    
    def test_get_report_summary_half_yearly(self, client, init_database):
        """Test getting half-yearly report summary."""
        response = client.get('/api/reports/summary?period=half-yearly')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['period'] == 'half-yearly'
    
    def test_get_report_summary_yearly(self, client, init_database):
        """Test getting yearly report summary."""
        response = client.get('/api/reports/summary?period=yearly')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['period'] == 'yearly'
    
    def test_get_report_summary_custom_date_range(self, client, init_database):
        """Test getting report with custom date range."""
        start_date = (date.today() - timedelta(days=7)).isoformat()
        end_date = date.today().isoformat()
        
        response = client.get(
            f'/api/reports/summary?start_date={start_date}&end_date={end_date}'
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['start_date'] == start_date
        assert data['end_date'] == end_date
    
    def test_report_category_breakdown(self, client, init_database):
        """Test that category breakdown includes percentage."""
        response = client.get('/api/reports/summary?period=monthly')
        data = json.loads(response.data)
        
        for category in data['category_breakdown']:
            assert 'name' in category
            assert 'color' in category
            assert 'total' in category
            assert 'count' in category
            assert 'percentage' in category
    
    def test_report_expenses_list(self, client, init_database):
        """Test that report includes expense list."""
        response = client.get('/api/reports/summary?period=monthly')
        data = json.loads(response.data)
        
        assert 'expenses' in data
        assert isinstance(data['expenses'], list)


class TestChartData:
    """Tests for chart data endpoint."""
    
    def test_get_pie_chart_data(self, client, init_database):
        """Test getting pie chart data."""
        response = client.get('/api/reports/chart-data?chart_type=pie')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'labels' in data
        assert 'colors' in data
        assert 'data' in data
        assert len(data['labels']) == len(data['data'])
    
    def test_get_bar_chart_data(self, client, init_database):
        """Test getting bar chart data."""
        response = client.get('/api/reports/chart-data?chart_type=bar')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'labels' in data
        assert 'colors' in data
        assert 'data' in data
    
    def test_get_line_chart_data(self, client, init_database):
        """Test getting line chart data."""
        response = client.get('/api/reports/chart-data?chart_type=line')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'labels' in data
        assert 'data' in data


class TestExportExcel:
    """Tests for Excel export endpoint."""
    
    def test_export_excel(self, client, init_database):
        """Test exporting to Excel."""
        response = client.get('/api/reports/export/excel?period=monthly')
        
        assert response.status_code == 200
        assert 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in response.content_type
        assert response.data is not None
        assert len(response.data) > 0
    
    def test_export_excel_with_custom_dates(self, client, init_database):
        """Test exporting to Excel with custom date range."""
        start_date = (date.today() - timedelta(days=30)).isoformat()
        end_date = date.today().isoformat()
        
        response = client.get(
            f'/api/reports/export/excel?start_date={start_date}&end_date={end_date}'
        )
        
        assert response.status_code == 200


class TestExportPDF:
    """Tests for PDF export endpoint."""
    
    def test_export_pdf(self, client, init_database):
        """Test exporting to PDF."""
        response = client.get('/api/reports/export/pdf?period=monthly')
        
        assert response.status_code == 200
        assert 'application/pdf' in response.content_type
        assert response.data is not None
        assert len(response.data) > 0
    
    def test_export_pdf_with_custom_dates(self, client, init_database):
        """Test exporting to PDF with custom date range."""
        start_date = (date.today() - timedelta(days=30)).isoformat()
        end_date = date.today().isoformat()
        
        response = client.get(
            f'/api/reports/export/pdf?start_date={start_date}&end_date={end_date}'
        )
        
        assert response.status_code == 200
