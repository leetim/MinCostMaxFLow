#include <iostream>
#include <set>
#include <vector>
#include <string>
#include <memory>
using namespace std;
////////////////////////////////////////////////////////////////////////////////

class Edge;
struct Reference;
typedef shared_ptr<Edge> PEdge;
typedef shared_ptr<Reference> PReference;

int add_vert(Reference r);
void add_edge(PEdge e);
PEdge get_edge(int v, char c);
bool comb_sub_str(int i, int j, int n);
Reference go_to(int v, int k, int n);
bool check(int v, int k, int n, char c);
void add_list(int root, int k);
bool check_str(int root, string& s);

vector< vector<PEdge> > edges;
vector<Reference> reference;
string text;

////////////////////////////////////////////////////////////////////////////////
struct Reference{
  Reference(): v(-1), k(-1), n(-1){};
  Reference(const Reference& r): v(r.v), k(r.k), n(r.n){};
  Reference(int _v, int _k, int _n): v(_v), k(_k), n(_n){};
  void print(){
    cout << "(" << v << " " << k << " " << n << ")" << endl;
  }
  int v;
  int k;
  int n;
};

////////////////////////////////////////////////////////////////////////////////
class Edge{
public:
  Edge(): src(-1), to(-1), k(-1), n(-1){};
  Edge(int _src, int _to, int _k, int _n): src(_src), to(_to), k(_k), n(_n){};
  int div(int num){
    Reference r = reference[src];
    if (r.n == 0){
      r = go_to(r.v, k, num);
    }
    else{
      r = go_to(r.v, r.k, r.n + num);
    }
    int v = add_vert(r);
    PEdge ne = PEdge(new Edge(v, to, k+num, n-num));
    to = v;
    n = num;
    add_edge(ne);
    return v;
  }
  int src;
  int to;
  int k;
  int n;
};


////////////////////////////////////////////////////////////////////////////////
int add_vert(Reference r){
  int i = edges.size();
  vector<PEdge> eds(26);
  edges.push_back(eds);
  reference.push_back(r);
  return i;
}

////////////////////////////////////////////////////////////////////////////////
void add_edge(PEdge e){
  edges[e->src][(int)(text[e->k] - 'a')] = e;
}

////////////////////////////////////////////////////////////////////////////////
PEdge get_edge(int v, char c){
  return edges[v][(int)(c - 'a')];
}

////////////////////////////////////////////////////////////////////////////////
bool comp_sub_str(int i, int j, int n){
  if (i == j){
    return true;
  }
  for (int k = 0; k < n; k++){
    if (text[i+k] != text[j+k]){
      return false;
    }
  }
  return true;
}

////////////////////////////////////////////////////////////////////////////////
Reference go_to(int v, int k, int n){
  if (n == 0){
    return Reference(v, k, n);
  }
  PEdge e = get_edge(v, text[k]);
  if (!e){
    return Reference();
  }
  if (e->n == 1 && e->k == -1){
    return go_to(e->to, k+1, n-1);
  }
  if (n >= e->n && text[k] == text[e->k]){
    return go_to(e->to, k+e->n, n-e->n);
  }
  if (n < e->n && text[k] == text[e->k]){
    return Reference(v, k, n);
  }
}

////////////////////////////////////////////////////////////////////////////////
bool check(int v, int k, int n, char c){
  if (n == 0){
    PEdge e = get_edge(v, c);
    return !(bool)e;
  }
  else{
    PEdge e = get_edge(v, text[k]);
    if (e){
      return text[e->k+n] != c;
    }
  }
  return true;
}

////////////////////////////////////////////////////////////////////////////////
void add_list(int root, int k){
  add_edge(PEdge(new Edge(root, -1, k, text.size() - k)));
}

////////////////////////////////////////////////////////////////////////////////
bool check_str(int root, string& s){
  for (int i = 0; i < s.size();){
    int temp = root;
    PEdge e = get_edge(root, s[i]);
    if (!e){
      return false;
    }
    if (i + e->n <= s.size() && text.substr(e->k, e->n) == s.substr(i, e->n)){
      root = e->to;
      i += e->n;
      continue;
    }
    if (i + e->n > s.size() && text.substr(e->k, s.size() - i) == s.substr(i, s.size() - i)){
      return true;
    }
    if (temp == root){
      return false;
    }
  }
  return true;
}

void print_tree(){
  for (int i = 0; i < edges.size(); i++){
    cout << i << ") ";
    for (auto j: edges[i]){
      if (j){
        cout << "[" << j->to << ", " << text.substr(j->k, j->n) << "] ";
      }
    }
    cout << endl;
  }
}

////////////////////////////////////////////////////////////////////////////////
int main(){
  freopen("input.txt", "r", stdin);
  freopen("output.txt", "w", stdout);
  cin >> text;
  int n;
  cin >> n;
  vector<string> requests(n);
  for (int i = 0; i < n; i++){
    cin >> requests[i];
  }
  int dig = add_vert(Reference(0, -1, 0));
  reference[dig] = Reference(dig, -1, 0);
  int root = add_vert(Reference(dig, -1, 0));
  set<char> chars;
  vector<int> pos(26);
  for (int i = 0; i < text.size(); i++){
    chars.insert(text[i]);
    pos[text[i] - 'a'] = i;
  }
  for (auto c: chars){
    add_edge(PEdge(new Edge(dig, root, pos[c - 'a'], 1)));
  }
  Reference ep(root, -1, 0);
  for (int i = 0; i < text.size(); i++){
    Reference ap = ep;
    char c = text[i];
    while (check(ap.v, ap.k, ap.n, c)){
      if (ap.n != 0){
        PEdge e = get_edge(ap.v, text[ap.k]);
        ap.v = e->div(ap.n);
      }
      add_list(ap.v, i);
      reference[ap.v] = go_to(reference[ap.v].v, reference[ap.v].k, reference[ap.v].n);
      ap = reference[ap.v];
    }
    if (ap.n == 0){
      ep = go_to(ap.v, i, 1);
    }
    else{
      ep = go_to(ap.v, ap.k, ap.n+1);
    }
  }
  for (auto s: requests){
    cout << check_str(root, s) << " ";
  }
  cout << endl;
  return 0;
}
