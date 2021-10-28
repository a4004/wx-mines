#pragma once
#include "wx/wx.h"
 
class cMain : public wxFrame
{
public:
	cMain();
	~cMain();
public:
	//wxButton* m_btn1	= nullptr;
	//wxTextCtrl* m_txt1	= nullptr;
	//wxListBox* m_list1	= nullptr;

	//void OnButtonClicked(wxCommandEvent& evt);

	//wxDECLARE_EVENT_TABLE();
public:
	int nFieldWidth		= 10;
	int nFieldHeight	= 10;
	wxButton** arr_btn;

	int* nField			= nullptr;
	bool bFirstClick	= true;
	bool bLost			= false;

	void OnButtonGridClicked(wxCommandEvent& evt);
};

