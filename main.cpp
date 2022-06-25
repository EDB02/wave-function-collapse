#include "includes/json.hpp"
#include <bits/stdc++.h>

#pragma GCC optimize("O3,unroll-loops")
#pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")

using json = nlohmann::json;
using namespace std;

#define pii pair<int, int>

json dic;
const int images = 14;
const int msize = 20;


struct cell{
    bool *p;         //possibili
    vector<vector<int> > near;
    int cnt;       //rimanenti
    bool done;
};

bool rest = 0;
clock_t start;

cell matrix[msize][msize];
int allcheck = msize*msize;
priority_queue<pair<int, pair<int, pair<int, int> > > > pq;

void mremove(int x, int y, int i);
void init();
pii getMin();
void setRandom(int x, int y);
string getFinal(cell c);
void mremove(int x, int y, int i);
void print();
void time(){
    cout<<((double)clock()-start)/(double)CLOCKS_PER_SEC<<endl;
}

int main(){
    srand(time(NULL));
    freopen("out.txt", "w", stdout);
    std::ifstream ifs("connections.json");
    std::string content( (std::istreambuf_iterator<char>(ifs)),(std::istreambuf_iterator<char>()));
    dic = json::parse(content);

    start = clock();

    rest = 1;
    int attempt = 0;

    while(rest){
        rest = 0;
        attempt++;
        allcheck = msize*msize;
        init();
        while(!rest && allcheck){
            pii tmp = getMin();
            setRandom(tmp.first, tmp.second);
            if(rest) break;
            allcheck-=!matrix[tmp.first][tmp.second].done;
            matrix[tmp.first][tmp.second].done = 1;
        }
        if(attempt > 1e5) break;
    }
    print();
    cout<<"attempts: "<<attempt<<endl;
    time();
}

cell initial;
bool ck = 0;

void init(){
    while(pq.size()) pq.pop();
    if(ck){
        for(int i=0;i<msize;i++){
            for(int j=0;j<msize;j++){
                matrix[i][j].cnt = initial.cnt;
                matrix[i][j].done = initial.done;
                matrix[i][j].near.resize(4);
                for(int k=0;k<4;k++) matrix[i][j].near[k] = initial.near[k];
                copy(initial.p, initial.p+images, matrix[i][j].p);
                pq.push({-matrix[i][j].cnt, {rand()%1000, {i, j}}});
            }
        }
    }
    else{
        ck = 1;
        initial.cnt = images;
        initial.p = new bool[images];
        initial.done = 0;
        fill_n(initial.p, images, 1);

        
        for(int i=0;i<msize;i++)
            for(int j=0;j<msize;j++) matrix[i][j].p = new bool[images];

        string at, bt;
        
        initial.near.resize(4);
        for(int k=0;k<4;k++){
            initial.near[k].resize(images);
            fill(initial.near[k].begin(), initial.near[k].end(), 0);
            for(int l=0;l<images;l++){
                at = to_string(l+1);
                bt = "l"+to_string(k);
                for(int h:dic[at][bt]){
                    initial.near[k][h-1]++;
                }
            }
        }
        init();
        return;
    }
}

pii getMin(){
    int x, y;
    do{
        x = pq.top().second.second.first;
        y = pq.top().second.second.second;
        pq.pop();
    }while(pq.size() && matrix[x][y].done);
    return {x, y};
}

void setRandom(int x, int y){
    if(matrix[x][y].cnt < 1){
        rest = 1;
        return;
    }
    int i;
    int r = rand()%matrix[x][y].cnt;
    for(i=0;i<images && r;i++){
        if(matrix[x][y].p[i]){
            mremove(x, y, i);
            r--;
        }
    }
    for(;i<images;i++){
        if(matrix[x][y].p[i]){
            i++;
            break;
        }
    }
    for(;i<images;i++){
        if(matrix[x][y].p[i]){
            mremove(x, y, i);
            r--;
        }
    }
}

string getFinal(cell c){
    string ris = "";
    for(int i=0;i<images;i++){
        if(c.p[i]) ris += to_string(i+1) + " ";
    }
    if(ris == ""){
        return "0";
    }
    return ris;
}

void mremove(int x, int y, int i){
    queue<pair<pair<int, int>, int> > st;

    st.push({{x, y}, i});

    while(st.size()){
        x = st.front().first.first;
        y = st.front().first.second;
        i = st.front().second;
        st.pop();
        if(x < 0 || x >= msize || y < 0 || y >= msize || i < 0 || i >= images || !matrix[x][y].p[i]) continue;
        matrix[x][y].p[i] = 0;
        matrix[x][y].cnt--;
        if(matrix[x][y].cnt < 1){
            rest = 1;
            return;
        }
        pq.push({-matrix[x][y].cnt, {rand()%1000, {x, y}}});
        int posx, posy;
        for(int j=0;j<4;j++){
            for(int k:dic[to_string(i+1)]["l"+to_string(j)]){
                matrix[x][y].near[j][k-1]--;
                if(matrix[x][y].near[j][k-1] <= 0){
                    posx = j==1?x+1:(j==3?x-1:x);
                    posy = j==0?y-1:(j==2?y+1:y);
                    st.push({{posx, posy}, k-1});
                }
            }
        }
    }
}

void print(){
    cout<<msize<<endl;
    for(int i=0;i<msize;i++){
        cout<<getFinal(matrix[i][0]);
        for(int j=1;j<msize;j++){
            cout<<"|"<<getFinal(matrix[i][j]);
        }
        cout<<endl;
    }
    cout<<endl;
}
