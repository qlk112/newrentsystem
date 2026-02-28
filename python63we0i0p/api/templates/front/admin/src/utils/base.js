const base = {
    get() {
        return {
            url : "http://localhost:5001/python63we0i0p/",
            name: "python63we0i0p",
            // 退出到首页链接
            indexUrl: 'http://localhost:5001/front/dist/index.html'
        };
    },
    getProjectName(){
        return {
            projectName: "基于Hadoop的租房数据分析系统的设计与实现"
        } 
    }
}
export default base
