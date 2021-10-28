#include "cMain.h"

//wxBEGIN_EVENT_TABLE(cMain, wxFrame)
	//EVT_BUTTON(10001, OnButtonClicked)
//wxEND_EVENT_TABLE()

cMain::cMain() : wxFrame(nullptr, wxID_ANY, "wxMinesweeper", wxPoint(30, 30), wxSize(400, 600))
{
	//m_btn1 = new wxButton(this, 10001, "Add to shopping list", wxPoint(10, 10), wxSize(150, 50));
	//m_txt1 = new wxTextCtrl(this, wxID_ANY, "", wxPoint(10, 70), wxSize(300, 30));
	//m_list1 = new wxListBox(this, wxID_ANY, wxPoint(10, 110), wxSize(300, 300));

	arr_btn = new wxButton*[nFieldWidth * nFieldHeight];
	wxGridSizer* grid = new wxGridSizer(nFieldWidth, nFieldHeight, 0, 0);

	nField = new int[nFieldWidth * nFieldHeight];

	wxFont font(24, wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_BOLD, false);

	for (int x = 0; x < nFieldWidth; x++) 
	{
		for (int y = 0; y < nFieldHeight; y++)
		{
			arr_btn[y * nFieldWidth + x] = new wxButton(this, 10000 + (y * nFieldWidth + x));
			arr_btn[y * nFieldWidth + x]->SetFont(font);
			grid->Add(arr_btn[y * nFieldWidth + x], 1, wxEXPAND | wxALL);

			arr_btn[y * nFieldWidth + x]->Bind(wxEVT_COMMAND_BUTTON_CLICKED, &cMain::OnButtonGridClicked, this);
			nField[y * nFieldWidth + x] = 0;
		}
	}

	this->SetSizer(grid);
	grid->Layout();
}

cMain::~cMain()
{
}

void cMain::OnButtonGridClicked(wxCommandEvent& evt)
{
	int x = (evt.GetId() - 10000) % nFieldWidth;
	int y = (evt.GetId() - 10000) / nFieldWidth;

	if (bFirstClick)
	{
		int mines = 30;

		while (mines)
		{
			int rx = rand() % nFieldWidth;
			int ry = rand() % nFieldHeight;

			if (nField[ry * nFieldWidth + rx] == 0 && rx != x && ry != y)
			{
				nField[ry * nFieldWidth + rx] = -1;
				mines--;
			}
		}

		bFirstClick = false;
	}

	//							->Enable(false);
	//arr_btn[y * nFieldWidth + x]->Unbind(wxEVT_COMMAND_BUTTON_CLICKED, OnButtonGridClicked);

	arr_btn[y * nFieldWidth + x]->Enable(false);

	if (nField[y * nFieldWidth + x] == -1)
	{
		//if(!bLost)

		for (int x = 0; x < nFieldWidth; x++)
		{
			for (int y = 0; y < nFieldHeight; y++)
			{
				if(nField[y * nFieldWidth + x] == -1) 
					arr_btn[y * nFieldWidth + x]->SetLabel("X");
			}
		}

		wxMessageBox("You landed on a mine!", ":(");

		//arr_btn[y * nFieldWidth + x]->SetBackgroundColour(wxColour(*wxRED));

		//bLost = true;

		// clear all buttons

		bFirstClick = true;

		for (int x = 0; x < nFieldWidth; x++)
		{
			for (int y = 0; y < nFieldHeight; y++)
			{
				nField[y * nFieldWidth + x] = 0;
				arr_btn[y * nFieldWidth + x]->SetLabel("");
				arr_btn[y * nFieldWidth + x]->Enable(true);
			}
		}
	}
	else
	{
		//arr_btn[y * nFieldWidth + x]->SetBackgroundColour(wxColour(*wxGREEN));

		// count neighbouring mines

		int mine_count = 0;

		for (int i = -1; i < 2; i++)
		{
			for (int j = -1; j < 2; j++)
			{
				if (x + i >= 0 && x + i < nFieldWidth && y + j >= 0 && y + j < nFieldHeight)
				{
					if (nField[(y + j) * nFieldWidth + (x + i)] == -1)
						mine_count++;
				}
			}
		}

		if (mine_count == 0)
			arr_btn[y * nFieldWidth + x]->SetLabel(":)");
		else
			arr_btn[y * nFieldWidth + x]->SetLabel(std::to_string(mine_count));
	}


	evt.Skip();
}

/*
void cMain::OnButtonClicked(wxCommandEvent& evt)
{
	m_list1->AppendString(m_txt1->GetValue());
	evt.Skip();
}
*/